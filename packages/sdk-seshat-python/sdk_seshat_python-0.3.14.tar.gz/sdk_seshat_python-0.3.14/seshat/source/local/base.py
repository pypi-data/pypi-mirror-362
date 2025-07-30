from seshat.data_class import SFrame
from seshat.general import configs
from seshat.source import Source


class LocalSource(Source):
    """
    LocalSource is a source that can read data from csv file.
    """

    def __init__(
        self,
        path,
        query=None,
        schema=None,
        mode=configs.DEFAULT_MODE,
    ):
        super().__init__(query, schema, mode)
        self.path = path

    def convert_data_type(self, data) -> SFrame:
        return self.data_class.from_raw(data)

    def fetch(self) -> SFrame:
        d = self.data_class.read_csv(path=self.path)
        return self.convert_data_type(d)

    def calculate_complexity(self):
        return 10
