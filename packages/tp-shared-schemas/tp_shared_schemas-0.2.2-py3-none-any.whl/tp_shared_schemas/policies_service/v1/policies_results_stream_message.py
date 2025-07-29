from datetime import date
from enum import Enum

from tp_shared_schemas.base import BaseMessage


class PolicySeries(str, Enum):
    XXX = "ХХХ"
    TTT = "ТТТ"
    AAA = "ААА"
    AAV = "ААВ"
    AAK = "ААК"
    AAM = "ААМ"
    AAN = "ААН"
    AAS = "ААС"
    VVV = "ВВВ"
    EEE = "ЕЕЕ"
    KKK = "ККК"
    MMM = "МММ"
    NNN = "ННН"
    RRR = "РРР"
    SSS = "ССС"


class PolicyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    WAITING_ACTIVATION = "WAITING_ACTIVATION"
    EXPIRED = "EXPIRED"


class PolicyResultItem(BaseMessage):
    series: PolicySeries
    number: str
    status: PolicyStatus
    start_date: date
    end_date: date
    period1_start: date
    period1_end: date
    period2_start: date
    period2_end: date
    period3_start: date
    period3_end: date
    vin: str
    car_mark: str
    car_model: str


class PoliciesResultsStreamMessage(BaseMessage):
    version = "1.0"
    reg_number: str
    policies: list[PolicyResultItem] = []
