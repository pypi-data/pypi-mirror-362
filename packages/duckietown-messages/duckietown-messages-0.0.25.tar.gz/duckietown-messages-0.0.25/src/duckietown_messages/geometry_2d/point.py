from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Point(BaseMessage):
    header: Header = AUTO

    x: float = Field(description="X coordinate of the point")
    y: float = Field(description="Y coordinate of the point")
