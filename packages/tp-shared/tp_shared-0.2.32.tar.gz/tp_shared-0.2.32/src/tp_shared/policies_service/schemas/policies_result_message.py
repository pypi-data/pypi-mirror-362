from datetime import date

from tp_shared.base.base_message import BaseMessage
from tp_shared.types.policy_series import PolicySeries
from tp_shared.types.policy_status import PolicyStatus


class PoliciesResultPolicy(BaseMessage):
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


class PoliciesResultMessage(BaseMessage):
    version: str = "1.0"
    reg_number: str
    policies: list[PoliciesResultPolicy] = []
