from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class Dictionary(BaseMessage):
    header: Header = AUTO

    data: dict = Field(description="Dictionary payload")
