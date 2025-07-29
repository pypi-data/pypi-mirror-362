from pydantic import Field
from ..base import BaseMessage

class DroneControl(BaseMessage):
    """
    Roll Pitch Yaw(rate) Throttle Commands, simulating output from
    remote control. Values range from 900 to 2000
    which corespond to values from 0% to 100%
    """
    roll: float = Field(description="Roll command", le=2000, ge=900)
    pitch: float = Field(description="Pitch command", le=2000, ge=900)
    yaw: float = Field(description="Yaw command", le=2000, ge=900)
    throttle: float = Field(description="Throttle command", le=2000, ge=900)