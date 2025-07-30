from enum import Enum


class AbstractDataContractKind(str, Enum):
    DATACONTRACT = "DataContract"

    def __str__(self) -> str:
        return str(self.value)
