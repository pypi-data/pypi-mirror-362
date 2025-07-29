from typing import List

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO
from ..standard.pair import Pair


class DCMotorCalibration(BaseMessage):
    header: Header = AUTO

    gain: List[Pair[float, float]] = Field(description="Gain of the motor as a list of "
                                                       "pairs (commanded PWM, correction factor). Always apply "
                                                       "the correction factor of the closest commanded PWM value.")
