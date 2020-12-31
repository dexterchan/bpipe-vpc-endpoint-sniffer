from __future__ import annotations
from typing import Protocol, List
from .model import BpipeEndpoint

class BpipeEndPointListWriter(Protocol):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def write_BpipeEndpoint_list_to_messagebus(self, bpipeEndpointLst:List[BpipeEndpoint])->None:
        ...

