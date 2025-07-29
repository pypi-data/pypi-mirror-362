from typing import Optional

from ....base import BaseMessage
from ....network.dtps.context import DTPSContextMsg


class HILConnectionConfiguration(BaseMessage):
    # simulator
    simulator: Optional[DTPSContextMsg] = None

    # agent information
    agent_name: str

    def __str__(self):
        return "HILConnectionConfiguration(simulator=%s, agent_name=%r,)" % (self.simulator, self.agent_name)
