from typing import List

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Homography(BaseMessage):
    header: Header = AUTO

    data: List[float] = Field(description="Homography matrix (flattened)")
