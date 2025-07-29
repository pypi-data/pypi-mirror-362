from typing import Optional

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Sensor(BaseMessage):
    # header
    header: Header = AUTO

    # the name of the sensor (e.g., "front_camera")
    name: str = Field(description="The name of the sensor")

    # the type of the sensor (e.g., "camera")
    type: str = Field(description="The type of the sensor")

    # whether the sensor is simulated
    simulated: bool = Field(description="Whether the sensor is simulated")

    # a description of the sensor
    description: Optional[str] = Field(description="A detailed description of the sensor", default=None)

    # the frame id of the sensor
    frame_id: Optional[str] = Field(description="The frame id of the sensor", default=None)

    # the frequency of the sensor
    frequency: Optional[float] = Field(description="The (expected) frequency of the sensor", default=None)

    # the maker of the sensor
    maker: Optional[str] = Field(description="The maker of the sensor", default=None)

    # the model of the sensor
    model: Optional[str] = Field(description="The model of the sensor", default=None)
