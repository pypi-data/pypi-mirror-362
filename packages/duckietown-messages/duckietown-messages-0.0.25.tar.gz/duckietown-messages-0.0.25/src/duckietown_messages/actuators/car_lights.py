from pydantic import Field

from ..base import BaseMessage
from ..colors.rgba import RGBA
from ..standard.header import Header, AUTO


class CarLights(BaseMessage):
    # header
    header: Header = AUTO

    # lights
    front_left: RGBA = Field(description="Front left light color and intensity")
    front_right: RGBA = Field(description="Front right light color and intensity")
    back_left: RGBA = Field(description="Back left light color and intensity")
    back_right: RGBA = Field(description="Back right light color and intensity")
