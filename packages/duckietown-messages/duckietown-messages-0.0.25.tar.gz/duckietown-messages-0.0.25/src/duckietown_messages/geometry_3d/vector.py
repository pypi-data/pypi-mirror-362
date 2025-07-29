import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Vector3(BaseMessage):
    header: Header = AUTO

    x: float = Field(description="X component")
    y: float = Field(description="Y component")
    z: float = Field(description="Z component")

    @classmethod
    def from_p(cls, p: np.ndarray, header: Header = None) -> 'Vector3':
        return cls(
            header=header or Header(),
            x=float(p[0]),
            y=float(p[1]),
            z=float(p[2]),
        )
