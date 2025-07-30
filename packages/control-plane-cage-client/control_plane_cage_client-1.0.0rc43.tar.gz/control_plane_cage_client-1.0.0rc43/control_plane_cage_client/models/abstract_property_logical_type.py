from enum import Enum


class AbstractPropertyLogicalType(str, Enum):
    BOOLEAN = "boolean"
    DATE = "date"
    INTEGER = "integer"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
