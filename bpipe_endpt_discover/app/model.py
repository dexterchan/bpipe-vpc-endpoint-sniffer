from pydantic import BaseModel
"""
class BpipeFeature(BaseModel):
    BusinessUnit: str
    Environment: str
"""

class BpipeEndpoint(BaseModel):
    hostname: str
    bpipe_id: str
