from __future__ import annotations

from typing import List, Protocol, Dict
from .model import BpipeEndpoint

class BpipeEndpointSniffer(Protocol):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def sniff_bpipe_endpoints(self, bpipeTags:Dict)->List[BpipeEndpoint]:
        ...