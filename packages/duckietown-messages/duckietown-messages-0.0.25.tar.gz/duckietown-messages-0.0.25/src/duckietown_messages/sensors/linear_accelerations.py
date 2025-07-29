from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class LinearAccelerations(BaseMessage):
    # header
    header: Header = AUTO

    # linear acceleration along the 3 axis
    x: float = Field(description="Linear acceleration along the x axis")
    y: float = Field(description="Linear acceleration along the y axis")
    z: float = Field(description="Linear acceleration along the z axis")
