import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Quaternion(BaseMessage):
    header: Header = AUTO

    w: float = Field(description="W component of the quaternion")
    x: float = Field(description="X component of the quaternion")
    y: float = Field(description="Y component of the quaternion")
    z: float = Field(description="Z component of the quaternion")

    @classmethod
    def from_q(cls, q: np.ndarray, header: Header = None) -> 'Quaternion':
        return cls(
            header=header or Header(),
            w=float(q[0]),
            x=float(q[1]),
            y=float(q[2]),
            z=float(q[3]),
        )
