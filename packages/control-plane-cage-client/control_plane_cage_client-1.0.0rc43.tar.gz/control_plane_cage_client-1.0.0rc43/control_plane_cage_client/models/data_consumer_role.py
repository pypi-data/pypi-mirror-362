from enum import Enum


class DataConsumerRole(str, Enum):
    DATACONSUMER = "DataConsumer"

    def __str__(self) -> str:
        return str(self.value)
