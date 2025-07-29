from duckietown_messages.base import BaseMessage
from pydantic import Field


class AttitudePIDParameters(BaseMessage):
    
    roll_pid_kp: float = Field(description="Roll PID proportional gain")
    roll_pid_ki: float = Field(description="Roll PID integral gain")
    roll_pid_kd: float = Field(description="Roll PID derivative gain")
    
    pitch_pid_kp: float = Field(description="Pitch PID proportional gain")
    pitch_pid_ki: float = Field(description="Pitch PID integral gain")
    pitch_pid_kd: float = Field(description="Pitch PID derivative gain")
    
    yaw_pid_kp: float = Field(description="Yaw PID proportional gain")
    yaw_pid_ki: float = Field(description="Yaw PID integral gain")
    yaw_pid_kd: float = Field(description="Yaw PID derivative gain")
