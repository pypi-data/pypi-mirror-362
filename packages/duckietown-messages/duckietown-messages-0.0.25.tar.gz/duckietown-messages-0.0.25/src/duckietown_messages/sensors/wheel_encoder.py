from pydantic import Field

from .generic import Sensor
from ..standard.header import Header, AUTO


class WheelEncoder(Sensor):
    header: Header = AUTO

    resolution: int = Field(description="Number of ticks per revolution", ge=0)
