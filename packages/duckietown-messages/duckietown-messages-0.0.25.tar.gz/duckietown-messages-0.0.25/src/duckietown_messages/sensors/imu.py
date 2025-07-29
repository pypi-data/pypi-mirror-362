from typing import List, Optional
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO
from duckietown_messages.geometry_3d.quaternion import Quaternion
from duckietown_messages.sensors.angular_velocities import AngularVelocities
from duckietown_messages.sensors.linear_accelerations import LinearAccelerations

class Imu(BaseMessage):
    """Imu message, used to store the IMU data.
    Refer to the ROS message definition for more information.
    http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Imu.html
    """
    header : Header = AUTO
    
    orientation : Optional[Quaternion] = None
    orientation_covariance : Optional[List[float]] = Field(None, max_length=9, min_length=9)
    angular_velocity : Optional[AngularVelocities] = None
    angular_velocity_covariance : Optional[List[float]] = Field(None, max_length=9, min_length=9)
    linear_acceleration : Optional[LinearAccelerations] = None
    linear_acceleration_covariance : Optional[List[float]] = Field(None, max_length=9, min_length=9)