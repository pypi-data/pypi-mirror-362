from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class Float(BaseMessage):
    header: Header = AUTO

    data: float = Field(description="Floating point number payload")
