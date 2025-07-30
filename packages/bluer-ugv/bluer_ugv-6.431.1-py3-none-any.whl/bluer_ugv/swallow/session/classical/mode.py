from enum import Enum, auto


class OperationMode(Enum):
    NONE = auto()
    PREDICTION = auto()
    TRAINING = auto()
