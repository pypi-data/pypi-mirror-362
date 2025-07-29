from pydantic import Field

from .generic import Sensor


class RangeFinder(Sensor):
    # the size of the arc that the distance reading is valid for in randians. 0 corresponds to the x-axis of the sensor.
    fov: float = Field(description="The size of the arc in randians. 0 corresponds to an ideal beam along the x-axis.")

    # minimum range value (meters)
    minimum: float = Field(description="Minimum range value (meters)")

    # maximum range value (meters)
    maximum: float = Field(description="Maximum range value (meters)")
