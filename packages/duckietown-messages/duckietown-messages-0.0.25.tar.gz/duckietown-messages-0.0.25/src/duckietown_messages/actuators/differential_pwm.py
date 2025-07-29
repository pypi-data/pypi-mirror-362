from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class DifferentialPWM(BaseMessage):
    # header
    header: Header = AUTO

    # PWM signal magnitude between -1 and 1 for the left wheel
    left: float = Field(description="PWM signal magnitude between -1 and 1 for the left wheel", ge=-1, le=1)

    # PWM signal magnitude between -1 and 1 for the left wheel
    right: float = Field(description="PWM signal magnitude between -1 and 1 for the right wheel", ge=-1, le=1)
