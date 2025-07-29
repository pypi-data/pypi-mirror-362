from pydantic import Field

from .generic import Actuator


class LEDs(Actuator):
    # whether the LEDs are addressable individually
    addressable: bool = Field(description="Whether the LEDs are addressable individually")

    # the number of LEDs
    quantity: int = Field(description="The number of LEDs", ge=0)

    # colors of the LEDs
    colors: int = Field(description="The number of primitive colors implemented in the LED", ge=0)

    # resolution of the LEDs
    resolution: int = Field(description="The resolution of each color in number of bits", ge=0)
