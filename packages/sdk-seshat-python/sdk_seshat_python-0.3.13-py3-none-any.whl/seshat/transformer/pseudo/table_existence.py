from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.source.mixins import SQLMixin
from seshat.transformer import Transformer
from seshat.transformer.schema import Schema


class SQLTableExistenceValidator(Transformer, SQLMixin):
    HANDLER_NAME = "run"

    def __init__(
        self,
        schema: Schema,
        url: str,
        table_name: str,
        group_keys=None,
    ):
        super().__init__(group_keys)

        self.table_name = table_name
        self.schema = schema
        self.url = url

    def run_df(self, default: DataFrame, *args, **kwargs):
        self.ensure_table_exists(self.table_name, self.schema)
        return {"default": default}

    def run_spf(self, default: PySparkDataFrame, *args, **kwargs):
        self.ensure_table_exists(self.table_name, self.schema)
        return {"default": default}

    def calculate_complexity(self):
        return 10
