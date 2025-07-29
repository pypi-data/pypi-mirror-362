from typing import Optional

import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO

from .position import Position
from .quaternion import Quaternion


class Transformation(BaseMessage):
    header: Header = AUTO

    source: Optional[str] = Field(None, description="The frame id of the source frame")
    target: Optional[str] = Field(None, description="The frame id of the target frame")
    position: Position = Field(description="The position of the target frame in the source frame")
    rotation: Quaternion = Field(description="The rotation of the target frame in the source frame")

    @classmethod
    def from_pq(cls,
                pq: np.ndarray,
                source: Optional[str] = None,
                target: Optional[str] = None,
                header: Header = None) -> 'Transformation':
        p, q = pq[:3], pq[3:]
        return cls(
            header=header or Header(),
            source=source,
            target=target,
            position=Position.from_p(p),
            rotation=Quaternion.from_q(q),
        )
