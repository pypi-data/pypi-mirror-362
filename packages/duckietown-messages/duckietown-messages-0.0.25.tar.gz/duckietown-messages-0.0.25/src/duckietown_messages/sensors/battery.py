from typing import List
from pydantic import Field
from ..base import BaseMessage
from ..standard.header import Header, AUTO

class BatteryState(BaseMessage):
    """
    The BatteryState class represents the state of a battery.

    Attributes:
        header (Header): The header of the battery state message.
        voltage (float): The voltage of the battery.
        present (bool): True if the battery is present, False otherwise.
        charge (float): The current battery charge in Ah.
        capacity (float): The capacity of the battery in Ah.
        design_capacity (float): The design capacity of the battery in Ah.
        percentage (float): The battery charge percentage.
        power_supply_status (int): The power supply status.
        power_supply_health (int): The power supply health.
        power_supply_technology (int): The power supply technology.
        cell_voltage (List[float]): An array of individual cell voltages for each cell in the battery.
        location (str): The location of the battery.
        serial_number (str): The serial number of the battery.
    """

    header: Header = AUTO
    voltage: float = Field(description="Voltage of the battery", ge=-1, default=0.0)
    present: bool = Field(description="True if the battery is present, False otherwise", default=False)
    charge: float = Field(description="Current battery charge in Ah", ge=0, default=0.0)
    capacity: float = Field(description="Capacity of the battery in Ah", ge=0, default=0.0)
    design_capacity: float = Field(description="Design capacity of the battery in Ah", ge=0, default=0.0)
    percentage: float = Field(description="Battery charge percentage", ge=0, le=100, default=0.0)
    power_supply_status: int = Field(description="Power supply status", ge=0, le=3, default=0)
    power_supply_health: int = Field(description="Power supply health", ge=0, le=3, default=0)
    power_supply_technology: int = Field(description="Power supply technology", ge=0, le=8, default=0)
    present: bool = Field(description="True if the battery is present, False otherwise", default=False)
    cell_voltage: List[float] = Field(description="Array of individual cell voltages for each cell in the battery", default=[])
    location: str = Field(description="Location of the battery", default="")
    serial_number: str = Field(description="Serial number of the battery", default="")
