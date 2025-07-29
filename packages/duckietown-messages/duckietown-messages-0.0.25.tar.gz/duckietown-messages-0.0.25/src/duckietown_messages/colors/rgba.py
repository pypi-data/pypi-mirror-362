from typing import List

from pydantic import Field

from duckietown_messages.base import BaseMessage
from duckietown_messages.standard.header import Header, AUTO


class RGBA(BaseMessage):
    header: Header = AUTO

    # intensities of the red, green, and blue components of the color in the range [0, 1]
    r: float = Field(description="Intensity of the red component of the color in the range [0, 1]", ge=0, le=1)
    g: float = Field(description="Intensity of the green component of the color in the range [0, 1]", ge=0, le=1)
    b: float = Field(description="Intensity of the blue component of the color in the range [0, 1]", ge=0, le=1)

    # alpha channel in the range [0, 1]
    a: float

    def __getitem__(self, item):
        return [self.r, self.g, self.b, self.a][item]

    @classmethod
    def zero(cls, header: Header = None) -> 'RGBA':
        return cls(
            header=header or Header(),
            r=0,
            g=0,
            b=0,
            a=0,
        )

    @classmethod
    def from_list(cls, lst: List[float], header: Header = None) -> 'RGBA':
        assert len(lst) == 4
        return cls(
            header=header or Header(),
            r=lst[0],
            g=lst[1],
            b=lst[2],
            a=lst[3],
        )

    @property
    def hex(self) -> str:
        return f"#{int(self.r * 255):02x}{int(self.g * 255):02x}{int(self.b * 255):02x}"
