
from attr import dataclass
from .privatelink import PrivateLinkBpipeEndpointSniffer
from .sqs_messagebus import SQSBpipeEndPointListWriter
from ..endptscanner import BpipeEndpointSniffer
from ..messagebus import BpipeEndPointListWriter

@dataclass
class AWSAdapter():
    bpipeEndPointSniffer: BpipeEndpointSniffer
    bpipeEndPointListWriter: BpipeEndPointListWriter


def aws_service_factory(queueURL:str) -> AWSAdapter:
    SQSBpipeEndPointListWriter(queueURL)

    bpipeEndPointSniffer = PrivateLinkBpipeEndpointSniffer()
    bpipeEndPointListWriter = SQSBpipeEndPointListWriter(queueURL)
    return AWSAdapter(
        bpipeEndPointSniffer, bpipeEndPointListWriter
    )



