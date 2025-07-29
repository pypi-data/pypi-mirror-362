from typing import Optional

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Actuator(BaseMessage):
    # header
    header: Header = AUTO

    # the name of the actuator (e.g., "left_motor")
    name: str = Field(description="The name of the actuator")

    # the type of the actuator (e.g., "motor")
    type: str = Field(description="The type of the actuator")

    # whether the actuator is simulated
    simulated: bool = Field(description="Whether the actuator is simulated")

    # a description of the actuator
    description: Optional[str] = Field(description="A detailed description of the actuator", default=None)

    # the frame id of the actuator
    frame_id: Optional[str] = Field(description="The frame id of the actuator", default=None)

    # the maker of the actuator
    maker: Optional[str] = Field(description="The maker of the actuator", default=None)

    # the model of the actuator
    model: Optional[str] = Field(description="The model of the actuator", default=None)
