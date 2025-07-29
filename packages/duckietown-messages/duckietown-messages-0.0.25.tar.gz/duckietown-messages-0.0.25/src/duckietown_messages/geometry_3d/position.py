import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Position(BaseMessage):
    header: Header = AUTO

    x: float = Field(description="X coordinate of the point")
    y: float = Field(description="Y coordinate of the point")
    z: float = Field(description="Z coordinate of the point")

    @classmethod
    def from_p(cls, p: np.ndarray, header: Header = None) -> 'Position':
        return cls(
            header=header or Header(),
            x=float(p[0]),
            y=float(p[1]),
            z=float(p[2]),
        )
