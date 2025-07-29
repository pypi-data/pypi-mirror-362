from typing import Generator, Dict, List, Any, Callable, TypeAlias

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd
from pandas import DataFrame
from pyspark.sql.dataframe import DataFrame as PySparkDataFrame

from seshat.data_class import DFrame
from seshat.general import configs
from seshat.profiler import track
from seshat.profiler.base import profiler
from seshat.transformer import Transformer
from seshat.utils.batcher import batch_pandas_df, batch_spark_df
from seshat.utils.clean_json import JSONCleaner

InputType: TypeAlias = List[Dict[str, Any]]
OutputType: TypeAlias = List[Dict[str, Any]]
ProcessResponseFn: TypeAlias = Callable[[InputType, InputType], OutputType]
ProcessBatchFn: TypeAlias = Callable[[List[List[Any]]], Dict[str, Any]]


class SFrameReducer(Transformer):
    HANDLER_NAME = "reduce"
    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}


class LLMInsightExtractor(SFrameReducer):
    """
    A transformer that extracts insights from data using Large Language Models (LLMs).

    This class leverages LLMs to analyze data and extract meaningful insights. It supports
    both batch processing and one-shot processing of data. The class can work with both
    pandas DataFrames and PySpark DataFrames.

    The insights extraction process involves sending data to an LLM with a template prompt,
    receiving the LLM's response, and processing that response into a structured format.
    The class supports grouping data before processing and can expand results based on IDs.

    Initialize the LLMInsightExtractor.

    Parameters
    ----------
    llm_client : BaseChatModel
        The LLM client used to generate insights.
    template_prompt : str
        The template prompt to send to the LLM. This should include placeholders for data.
    id_column : str, optional
        The column name to use as an identifier when expanding results. Required if expand_on_id is True.
    template_context : str, optional
        The system context to provide to the LLM. Defaults to a basic data scientist role.
    llm_input_columns : List[str], optional
        The columns to include in the data sent to the LLM. If None, all columns are included.
    process_llm_json_response_fn : ProcessResponseFn, optional
        A function to process the JSON response from the LLM.
    process_batch_fn : ProcessBatchFn, optional
        A function to process batches of data before sending to the LLM.
    process_llm_response : Callable, optional
        A function to process the raw LLM response before JSON parsing.
    retry : int, default=3
        The number of times to retry LLM calls on failure.
    batch_mode : bool, default=True
        Whether to process data in batches or all at once.
    chunk_size : int, optional, default=100
        The size of data batches when batched_mode is True.
    group_keys : dict, optional
        Keys to use for grouping data.
    group_by_columns : list[str], optional
        Columns to group data by before processing.
    group_by_inject_key : str, optional
        Key to inject group name into the template prompt. Requires group_by_columns.
    expand_on_id : bool, default=False
        Whether to expand results based on ID column. Requires id_column.
    inject_keys : dict[str, str], optional
        Additional keys to inject into the template prompt.

    Raises
    ------
    ValueError
        If group_by_inject_key is set but group_by_columns is not set,
        or if expand_on_id is True but id_column is not set.

    Examples
    --------
    Basic usage with a pandas DataFrame in batch mode::

        from langchain_openai import ChatOpenAI
        from seshat.transformer.reducer import LLMInsightExtractor

        # Prepare your DataFrame ``df`` here

        extractor = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt=
            Please analyse the following dataset and respond with a JSON list of insights.\n
            {inject_data}
            ,
            llm_input_columns=["question", "answer"],
        )

        # ``reduce`` always returns a dict keyed by ``group_keys`` (default is "default")
        insights_df = extractor.reduce(df)["default"]

    Grouped processing with ``group_by_columns`` and dynamic prompt injection::

        extractor_grouped = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-4o"),
            template_prompt="The following data belongs to the group: {country}. {inject_data}",
            group_by_columns=["country"],
            group_by_inject_key="country",
        )

        # Each country is processed separately and concatenated back together
        insights_df = extractor_grouped.reduce(df)["default"]

    One-shot processing (``batched_mode=False``)::

        extractor_one_shot = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt="Summarise this dataset: {inject_data}",
            batched_mode=False,
        )

        insights_df = extractor_one_shot.reduce(df)["default"]

    Using custom response post-processing::

        def post_process_llm_json(json_response: list[dict]):
            # Custom cleaning / validation
            return pd.DataFrame(json_response)

        extractor_custom = LLMInsightExtractor(
            llm_client=ChatOpenAI(model="gpt-3.5-turbo"),
            template_prompt="{inject_data}",
            process_llm_json_response_fn=post_process_llm_json,
        )
        insights_df = extractor_custom.reduce(df)["default"]
    """

    def __init__(
        self,
        llm_client: BaseChatModel,
        template_prompt: str,
        id_column: str = None,
        template_context: str = None,
        llm_input_columns: List[str] = None,
        process_llm_json_response_fn: ProcessResponseFn = None,
        process_batch_fn: ProcessBatchFn = None,
        process_llm_response: Callable = None,
        retry: int = 3,
        llm_result_cleaner: Callable = JSONCleaner().clean,
        batch_mode: bool = True,
        chunk_size: int | None = 100,
        group_keys=None,
        group_by_columns: list[str] = None,
        group_by_inject_key: str = None,
        expand_on_id: bool = False,
        inject_keys: dict[str, str] = None,
    ):

        super().__init__(group_keys)
        self.chunk_size = chunk_size
        self.llm_client = llm_client
        self.template_prompt = template_prompt
        self.process_llm_json_response_fn = process_llm_json_response_fn
        self.process_batch_fn = process_batch_fn
        self.retry = retry
        self.batch_mode = batch_mode

        self.cleaner = llm_result_cleaner

        self.llm_input_columns = llm_input_columns
        self.template_context = (
            template_context
            or """
            You are a data scientist.
            Your task is to analyze and provide insights about the given dataset.
        """
        )

        self.group_by_columns = group_by_columns
        self.id_column = id_column
        self.expand_on_id = expand_on_id
        self.inject_keys = inject_keys
        self.process_llm_response = process_llm_response
        self.group_by_inject_key = group_by_inject_key

        if self.group_by_inject_key and not self.group_by_columns:
            raise ValueError(
                "group_by_columns must be set if group_by_inject_key is set"
            )

        if self.expand_on_id and not self.id_column:
            raise ValueError("id_column must be set if expand_on_id is True")

    @track
    def ask_llm(self, prompt: str):
        """
        Send a prompt to the LLM and process the response.

        This method handles sending the prompt to the LLM, processing the response,
        and retrying on failure. It also validates that the response is a valid JSON list
        of dictionaries.

        Parameters
        ----------
        prompt : str
            The prompt to send to the LLM.

        Returns
        -------
        list[dict] or None
            A list of dictionaries containing the processed LLM response,
            or None if all retry attempts fail.

        Notes
        -----
        The method will retry up to self.retry times if an exception occurs.
        If self.process_llm_response is set, it will be used to process the raw LLM response.
        Otherwise, the method expects the LLM to return a JSON list of dictionaries.
        """
        retry_count = 0
        while retry_count < self.retry:
            try:
                messages = [
                    SystemMessage(content=self.template_context.strip()),
                    HumanMessage(content=prompt),
                ]

                llm_response = self.llm_client.invoke(messages)

                tokens_in = tokens_out = ""
                if hasattr(self.llm_client, "get_num_tokens"):
                    try:
                        prompt_for_count = "\n".join(
                            f"{m.type}:{m.content}" for m in messages
                        )
                        tokens_in = self.llm_client.get_num_tokens(prompt_for_count)
                        tokens_out = self.llm_client.get_num_tokens(
                            llm_response.content
                        )
                    except Exception:
                        pass

                profiler.log(
                    "info",
                    msg="llm_token_usage",
                    method=self.ask_llm.__wrapped__,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                )

                if self.process_llm_response:
                    return self.process_llm_response(llm_response)
                response_json = self.cleaner(llm_response.content)

                assert isinstance(
                    response_json, list
                ), f"{response_json} is not a valid json."
                assert all(
                    isinstance(item, dict) for item in response_json
                ), f"{response_json} is not a valid json."

                return response_json

            except Exception as e:
                retry_count += 1
                profiler.log(
                    "error",
                    msg="Response cannot be proceeded",
                    method=self.ask_llm.__wrapped__,
                    error=str(e),
                )

        return None

    @track
    def extract_insight_batch(
        self, data_batches: Generator[List[Dict[str, Any]], None, None], **kwargs
    ) -> DFrame:
        """
        Extract insights from batches of data.

        This method processes multiple batches of data, sending each batch to the LLM
        and collecting the responses. It supports various processing options including
        custom response processing, ID-based expansion, and group-based processing.

        Parameters
        ----------
        data_batches : Generator[List[Dict[str, Any]], None, None]
            A generator that yields batches of data as lists of dictionaries.
        **kwargs : dict
            Additional keyword arguments. Supported keys include:
            - group_name: The name of the current group when processing grouped data.

        Returns
        -------
        DFrame
            A DFrame containing the processed insights from all batches.

        Notes
        -----
        If self.process_llm_json_response_fn is set, it will be used to process each batch response.
        If self.expand_on_id is True, the method will expand the results based on the ID column.
        If self.group_by_inject_key is set and group_name is provided in kwargs, the group name
        will be injected into the template prompt.
        """
        batch_responses = []

        for batch_data in data_batches:
            format_args = {
                "inject_data": str(batch_data),
            }
            format_args.update(self.inject_keys or {})
            if kwargs.get("group_name") and self.group_by_inject_key:
                format_args[self.group_by_inject_key] = kwargs.get("group_name")

            if self.process_batch_fn and batch_responses:
                batch_data_dict = self.process_batch_fn(batch_responses)
                format_args.update(batch_data_dict)

            prompt = self.template_prompt.format(**format_args)
            llm_result = self.ask_llm(prompt=prompt)

            if llm_result:
                if self.process_llm_json_response_fn:
                    processed_result = self.process_llm_json_response_fn(
                        batch_data, llm_result
                    )
                    batch_responses.append(processed_result)
                elif self.expand_on_id:
                    reduce_df = pd.DataFrame(llm_result).explode(self.id_column)
                    input_df = pd.DataFrame(batch_data)
                    result = (
                        input_df.set_index(self.id_column)
                        .join(reduce_df.set_index(self.id_column), how="left")
                        .reset_index()
                    )
                    batch_responses.append(result)
                else:
                    batch_responses.append(llm_result)

        return DFrame(data=pd.concat(batch_responses, ignore_index=True))

    @track
    def extract_insight_one_shot(self, data: List[Dict[str, Any]], **kwargs) -> DFrame:
        """
        Extract insights from a single batch of data in one shot.

        This method processes a single batch of data, sending it to the LLM and processing
        the response. It supports various processing options including custom response
        processing, ID-based expansion, and group-based processing.

        Parameters
        ----------
        data : List[Dict[str, Any]]
            A list of dictionaries representing the data to process.
        **kwargs : dict
            Additional keyword arguments. Supported keys include:
            - group_name: The name of the current group when processing grouped data.

        Returns
        -------
        DFrame
            A DFrame containing the processed insights from the data.

        Notes
        -----
        If self.process_llm_json_response_fn is set, it will be used to process the LLM response.
        If self.expand_on_id is True, the method will expand the results based on the ID column.
        If self.group_by_inject_key is set and group_name is provided in kwargs, the group name
        will be injected into the template prompt.
        If the LLM returns no valid response, an empty DFrame is returned.
        """
        format_args = {"inject_data": str(data)}
        format_args.update(self.inject_keys or {})
        if kwargs.get("group_name") and self.group_by_inject_key:
            format_args[self.group_by_inject_key] = kwargs.get("group_name")

        prompt = self.template_prompt.format(**format_args)
        llm_result = self.ask_llm(prompt=prompt)

        if llm_result:
            if self.process_llm_json_response_fn:
                processed_data = self.process_llm_json_response_fn(data, llm_result)
                return DFrame(data=DataFrame(processed_data))
            elif self.expand_on_id:
                reduce_df = pd.DataFrame(llm_result).explode(self.id_column)
                input_df = pd.DataFrame(data)
                result = (
                    input_df.set_index(self.id_column)
                    .join(reduce_df.set_index(self.id_column), how="left")
                    .reset_index()
                )
                return DFrame(data=result)

            else:
                return DFrame(data=pd.DataFrame(llm_result))

        return DFrame(data=DataFrame([]))

    def reduce_df(self, default: DataFrame, **kwargs) -> Dict[str, DataFrame]:
        """
        Reduce a pandas DataFrame by extracting insights using an LLM.

        This method processes a pandas DataFrame, optionally grouping it by specified columns,
        and extracts insights using either batch processing or one-shot processing.

        Parameters
        ----------
        default : DataFrame
            The pandas DataFrame to process.
        **kwargs : dict
            Additional keyword arguments passed to extract_insight_batch or extract_insight_one_shot.

        Returns
        -------
        Dict[str, DataFrame]
            A dictionary with a single key 'default' mapping to the DataFrame containing
            the extracted insights.

        Notes
        -----
        If self.group_by_columns is set, the DataFrame will be grouped by those columns
        and each group will be processed separately.
        If self.llm_input_columns is set, only those columns will be included in the data
        sent to the LLM.
        If self.batched_mode is True, the data will be processed in batches using extract_insight_batch.
        Otherwise, it will be processed in one shot using extract_insight_one_shot.
        """
        groups = (
            default[[*self.group_by_columns]].drop_duplicates().to_dict("records")
            if self.group_by_columns
            else [None]
        )

        enriched_data_list = []
        for group in groups:
            if group is None:
                group_df = default
            else:
                mask = True
                for col, val in group.items():
                    mask &= default[col] == val
                group_df = default[mask]

            selected = (
                group_df[[*self.llm_input_columns]]
                if self.llm_input_columns
                else group_df
            )

            if self.batch_mode:
                group_enriched = self.extract_insight_batch(
                    data_batches=batch_pandas_df(selected, self.chunk_size),
                    group_name=group,
                    **kwargs,
                ).to_raw()
            else:
                group_enriched = self.extract_insight_one_shot(
                    data=selected.to_dict("records"),
                    group_name=group,
                    **kwargs,
                ).to_raw()

            enriched_data_list.append(group_enriched)

        if enriched_data_list:
            enriched_data = pd.concat(enriched_data_list, ignore_index=True)
        else:
            enriched_data = DataFrame([])

        return {"default": enriched_data}

    def reduce_spf(
        self, default: PySparkDataFrame, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        """
        Reduce a PySpark DataFrame by extracting insights using an LLM.

        This method processes a PySpark DataFrame, optionally grouping it by specified columns,
        and extracts insights using either batch processing or one-shot processing.

        Parameters
        ----------
        default : PySparkDataFrame
            The PySpark DataFrame to process.
        **kwargs : dict
            Additional keyword arguments passed to extract_insight_batch or extract_insight_one_shot.

        Returns
        -------
        Dict[str, PySparkDataFrame]
            A dictionary with a single key 'default' mapping to the PySpark DataFrame containing
            the extracted insights.

        Notes
        -----
        If self.group_by_columns is set, the DataFrame will be grouped by those columns
        and each group will be processed separately.
        If self.llm_input_columns is set, only those columns will be included in the data
        sent to the LLM.
        If self.batched_mode is True, the data will be processed in batches using extract_insight_batch.
        Otherwise, it will be processed in one shot using extract_insight_one_shot.
        The method handles the conversion between PySpark DataFrames and pandas DataFrames
        for processing and then converts back to PySpark for the final result.
        """
        groups = (
            default.select(*self.group_by_columns).distinct().toLocalIterator()
            if self.group_by_columns
            else [None]
        )

        enriched_data_list = []

        for group in groups:
            if group is None:
                group_df = default
            else:
                group_filter = " AND ".join(
                    [f"{col} = '{group[col]}'" for col in self.group_by_columns]
                )
                group_df = default.filter(group_filter)

            selected = (
                group_df.select(*self.llm_input_columns)
                if self.llm_input_columns
                else group_df
            )

            if self.batch_mode:
                group_enriched = (
                    self.extract_insight_batch(
                        data_batches=batch_spark_df(selected, self.chunk_size),
                        group_name=group,
                        **kwargs,
                    )
                    .to_spf()
                    .to_raw()
                )
            else:
                data = [row.asDict() for row in selected.toLocalIterator()]
                group_enriched = (
                    self.extract_insight_one_shot(data=data, group_name=group, **kwargs)
                    .to_spf()
                    .to_raw()
                )

            enriched_data_list.append(group_enriched)

        if enriched_data_list:
            enriched_data = enriched_data_list[0]
            for df in enriched_data_list[1:]:
                enriched_data = enriched_data.union(df)
        else:
            enriched_data = default.sparkSession.createDataFrame([], default.schema)

        return {"default": enriched_data}

    def calculate_complexity(self):
        return 80
