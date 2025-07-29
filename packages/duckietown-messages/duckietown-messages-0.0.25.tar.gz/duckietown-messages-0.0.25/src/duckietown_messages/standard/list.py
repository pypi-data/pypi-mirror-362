from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class List(BaseMessage):
    header: Header = AUTO

    data: list = Field(description="List payload")
