from ...base import BaseMessage


class HILConfiguration(BaseMessage):
    dreamwalking: bool = False

    def __str__(self):
        return "HILConfiguration(dreamwalking=%s)" % (self.dreamwalking)

