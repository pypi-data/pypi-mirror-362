from enum import Enum


class DataQualitySqlType(str, Enum):
    CUSTOM = "custom"
    LIBRARY = "library"
    SQL = "sql"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
