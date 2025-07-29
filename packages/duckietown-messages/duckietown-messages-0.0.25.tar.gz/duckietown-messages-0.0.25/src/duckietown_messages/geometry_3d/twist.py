from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO

from .vector import Vector3


class Twist(BaseMessage):
    header: Header = AUTO

    linear_velocity: Vector3 = Field(description="The velocity of the object")
    angular_velocity: Vector3 = Field(description="The angular velocity of the object")
