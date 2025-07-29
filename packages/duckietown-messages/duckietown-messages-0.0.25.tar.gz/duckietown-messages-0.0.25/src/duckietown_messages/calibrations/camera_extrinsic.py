from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class CameraExtrinsicCalibration(BaseMessage):
    header: Header = AUTO

    homography: list = Field(description="Homography matrix (flattened)")
