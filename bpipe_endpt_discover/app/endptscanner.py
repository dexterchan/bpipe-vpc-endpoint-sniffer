from __future__ import annotations

from typing import List, Protocol, Dict
from .model import BpipeEndpoint

class BpipeEndpointDiscover(Protocol):
    """
        Interface to discover all bpipe endpoint in an environment for next processing
    """
    def discover_bpipe_endpoints(self, bpipeTags:Dict)->List[BpipeEndpoint]:
        ...
