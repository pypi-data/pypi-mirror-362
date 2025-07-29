from typing import Optional

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class CameraIntrinsicCalibration(BaseMessage):
    header: Header = AUTO

    K: list = Field(description="Intrinsic camera matrix (flattened)")
    D: list = Field(description="Distortion coefficients")
    P: list = Field(description="Projection matrix (flattened)")
    R: Optional[list] = Field(description="Rectification matrix (flattened)", default=None)
