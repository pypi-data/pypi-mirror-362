from enum import Enum


class AbstractDataContractApiVersion(str, Enum):
    V2_2_0 = "v2.2.0"
    V2_2_1 = "v2.2.1"
    V2_2_2 = "v2.2.2"
    V3_0_0 = "v3.0.0"

    def __str__(self) -> str:
        return str(self.value)
