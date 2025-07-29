from typing import Union

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Range(BaseMessage):
    # header
    header: Header = AUTO

    # measured distance (meters, null if out-of-range)
    data: Union[float, None] = Field(None, description="Measured distance (meters, null if out-of-range)", ge=0)
