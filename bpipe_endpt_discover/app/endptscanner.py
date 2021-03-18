from __future__ import annotations

from typing import List, Protocol, Dict
from .model import BpipeEndpoint

class BpipeEndpointDiscover(Protocol):
    """
        Interface to discover all bpipe endpoint in an environment for next processing
        from give tag in event from json message field : "discover_tags"
    """
    def discover_bpipe_endpoints(self, bpipeTags:Dict)->List[BpipeEndpoint]:
        ...
