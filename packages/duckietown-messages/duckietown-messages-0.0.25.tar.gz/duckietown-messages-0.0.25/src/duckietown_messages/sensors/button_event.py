from enum import IntEnum

from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO


class InteractionEvent(IntEnum):
    NOTHING = 0
    SINGLE_CLICK = 1
    HELD_3SEC = 3
    HELD_10SEC = 10


class ButtonEvent(BaseMessage):
    # header
    header: Header = AUTO

    # event ID
    type: InteractionEvent = Field(description="Type of the event")
