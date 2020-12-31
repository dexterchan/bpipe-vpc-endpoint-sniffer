
from attr import dataclass
from .privatelink import PrivateLinkBpipeEndpointSniffer
from ..endptscanner import BpipeEndpointSniffer
from ..messagebus import BpipeEndPointListWriter

@dataclass
class AWSAdapter():
    bpipeEndPointSniffer: BpipeEndpointSniffer
    bpipeEndPointListWriter: BpipeEndPointListWriter


def aws_service_factory(queueURL:str) -> AWSAdapter:
    bpipeEndPointSniffer = PrivateLinkBpipeEndpointSniffer()
    bpipeEndPointListWriter = None
    return AWSAdapter(
        bpipeEndPointSniffer, bpipeEndPointListWriter
    )



