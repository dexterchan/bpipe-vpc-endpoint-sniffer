from pydantic import BaseModel
"""
Bpipe vpc endpoint (AWS)
hostname: hostname of vpc endppint
bpipe_id: Name tag of the vpc endpoint
"""

class BpipeEndpoint(BaseModel):
    hostname: str
    bpipe_id: str
