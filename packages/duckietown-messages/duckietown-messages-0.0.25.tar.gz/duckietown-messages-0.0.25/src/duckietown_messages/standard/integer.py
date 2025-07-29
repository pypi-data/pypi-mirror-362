from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class Integer(BaseMessage):
    header: Header = AUTO

    data: int = Field(description="Integer value payload")
