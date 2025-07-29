from pydantic import Field
from ..base import BaseMessage
from ..standard.header import AUTO, Header

class DroneMotorCommand(BaseMessage):
    """
    PWM commands from the range defined on betaflight for each motor.
    """
    header: Header = AUTO
    
    # range defined on cleanflight
    minimum : int = Field(description="Minimum PWM value for the motors", default=1000)
    maximum : int = Field(description="Maximum PWM value for the motors", default=2000)

    # PWM commands for the individual motors
    m1 : int = Field(description="PWM command for motor 1", default=1000)
    m2 : int = Field(description="PWM command for motor 2", default=1000)
    m3 : int = Field(description="PWM command for motor 3", default=1000)
    m4 : int = Field(description="PWM command for motor 4", default=1000)
