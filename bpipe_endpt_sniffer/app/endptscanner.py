from __future__ import annotations

from pydantic import BaseModel
from typing import Dict, List, Optional, Protocol


class BpipeFeature(BaseModel):
    BusinessUnit: str
    Environment: str

class BpipeEndpoint(BaseModel):
    hostname: str
    bpipe_id: str

class BpipeEndpointSniffer(Protocol):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def sniff_bpipe_endpoints(self, bpipeFeature:BpipeFeature)->List[BpipeEndpoint]:
        return NotImplementedError("Not implemented")