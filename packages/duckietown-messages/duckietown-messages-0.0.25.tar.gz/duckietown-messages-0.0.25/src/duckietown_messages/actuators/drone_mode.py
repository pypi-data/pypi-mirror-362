from enum import IntEnum

from pydantic import Field
from ..base import BaseMessage


class Mode(IntEnum):
    DISARMED = 0
    ARMED = 1
    FLYING = 2


class DroneModeMsg(BaseMessage):
    mode: Mode = Field(description="mode of the drone, can be DISARMED, ARMED, FLYING")


class DroneModeResponse(BaseMessage):
    previous_mode: Mode = Field(description="previous mode of the drone, can be DISARMED, ARMED, FLYING")
    current_mode: Mode = Field(description="current mode of the drone, can be DISARMED, ARMED, FLYING")