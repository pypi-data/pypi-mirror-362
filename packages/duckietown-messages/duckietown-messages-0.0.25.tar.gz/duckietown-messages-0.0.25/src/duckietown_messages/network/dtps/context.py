from typing import Union, List

from ...base import BaseMessage


class DTPSContextMsg(BaseMessage):
    # context configuration
    name: str
    urls: Union[List[str], None] = None
    path: Union[str, None] = None

    def __eq__(self, other):
        if not isinstance(other, DTPSContextMsg):
            return False
        return (self.name == other.name and
                sorted(self.urls or []) == sorted(other.urls or []) and
                (self.path or "").strip("/") == (other.path or "").strip("/"))

    def __str__(self):
        return "DTPSContextMsg(name=%r, urls=%r, path=%r)" % (self.name, self.urls, self.path)
