from enum import Enum


class DataProviderRole(str, Enum):
    DATAPROVIDER = "DataProvider"

    def __str__(self) -> str:
        return str(self.value)
