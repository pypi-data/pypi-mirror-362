from typing import TypeVar, Generic

from pydantic import BaseModel, Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


T1 = TypeVar("T1")
T2 = TypeVar("T2")


class Pair(BaseModel, Generic[T1, T2], BaseMessage):
    header: Header = AUTO

    first: T1 = Field(description="First element of the pair")
    second: T2 = Field(description="Second element of the pair")
