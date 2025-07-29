from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class AngularVelocities(BaseMessage):
    # header
    header: Header = AUTO

    # angular acceleration about the 3 axis
    x: float = Field(description="Angular velocities about the x axis [rad/s]")
    y: float = Field(description="Angular velocities about the y axis [rad/s]")
    z: float = Field(description="Angular velocities about the z axis [rad/s]")
