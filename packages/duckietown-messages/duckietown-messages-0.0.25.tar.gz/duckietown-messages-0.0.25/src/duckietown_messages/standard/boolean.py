from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class Boolean(BaseMessage):
    header: Header = AUTO

    data: bool = Field(description="Boolean value payload")
