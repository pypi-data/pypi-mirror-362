import enum
from datetime import date

from pydantic import ConfigDict

from tp_shared_schemas.base import BaseMessage


class GibddOperatorStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSE = "PAUSE"
    CANCEL = "CANCEL"


class GibddDcResultOperator(BaseMessage):
    operator_id: int
    status: GibddOperatorStatus
    name: str
    address_line: str
    phone_number: str
    email: str
    site: str
    canceled_date: date | None
    canceled_at: int | None


class GibddDcResultCard(BaseMessage):
    card_number: str
    vin: str
    start_date: date
    end_date: date
    odometer_value: int
    is_active: bool
    updated_at: int
    created_at: int

    operator: GibddDcResultOperator

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GibddDcResultsStreamMessage(BaseMessage):
    version = "1.0"
    vin: str
    diagnostic_cards: list[GibddDcResultCard] = []
