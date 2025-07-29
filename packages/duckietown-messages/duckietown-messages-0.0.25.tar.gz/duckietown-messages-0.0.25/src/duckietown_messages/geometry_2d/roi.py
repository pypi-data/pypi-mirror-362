from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class ROI(BaseMessage):
    # header
    header: Header = AUTO

    # height of ROI
    height: int = Field(description="Height of the region", ge=0)
    # width of ROI
    width: int = Field(description="Width of the region", ge=0)

    # leftmost pixel of the ROI (0 if the ROI includes the left edge of the image)
    x: int = Field(description="Leftmost pixel of the region", default=0, ge=0)
    # topmost pixel of the ROI (0 if the ROI includes the top edge of the image)
    y: int = Field(description="Topmost pixel of the region", default=0, ge=0)
