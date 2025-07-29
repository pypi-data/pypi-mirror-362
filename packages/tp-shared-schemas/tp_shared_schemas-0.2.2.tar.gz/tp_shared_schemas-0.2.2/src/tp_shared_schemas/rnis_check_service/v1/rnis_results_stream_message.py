from tp_shared_schemas.base import BaseMessage


class RNISCheckResultMessage(BaseMessage):
    version = "1.0"
    reg_number: str
    exists: bool
    last_mark: int | None
    terminals_amount: int
