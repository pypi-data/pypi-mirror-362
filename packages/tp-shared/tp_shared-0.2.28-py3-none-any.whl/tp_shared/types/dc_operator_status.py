import enum


class DcOperatorStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSE = "PAUSED"
    CANCEL = "CANCELLED"
