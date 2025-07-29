from pydantic import Field

from .generic import Sensor


class Camera(Sensor):
    width: int = Field(description="Width of the image", ge=0)
    height: int = Field(description="Height of the image", ge=0)

    fov: float = Field(description="Diagonal field of view of the camera in radians", ge=0)
