from __future__ import annotations

from typing import List, Protocol
from .model import BpipeEndpoint, BpipeFeature

class BpipeEndpointSniffer(Protocol):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def sniff_bpipe_endpoints(self, bpipeFeature:BpipeFeature)->List[BpipeEndpoint]:
        ...