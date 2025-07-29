from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class Temperature(BaseMessage):
    # header
    header: Header = AUTO

    # measured temperature (degrees Celsius)
    data: float = Field(description="Measured temperature (degrees Celsius)")
