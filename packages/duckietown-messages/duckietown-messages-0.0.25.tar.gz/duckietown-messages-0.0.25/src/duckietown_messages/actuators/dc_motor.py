from pydantic import Field

from .generic import Actuator


class DCMotor(Actuator):
    # voltage of the motor
    voltage: float = Field(description="Voltage of the motor", ge=0)

    # gear ratio of the motor
    gear_ratio: float = Field(description="Gear ratio of the motor", ge=0)

    # max torque of the motor
    torque: float = Field(description="Maximum torque of the motor", ge=0)

    # max speed of the motor (after gear ratio)
    speed: float = Field(description="Maximum speed of the motor in revolutions per second (after gearbox)", ge=0)
