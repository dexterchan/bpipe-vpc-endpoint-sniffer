
from attr import dataclass
from .privatelink import PrivateLinkBpipeEndpointSniffer
#from .sqs_messagebus import SQSBpipeEndPointListWriter
from .sns_messagebus import SNSBpipeEndPointListWriter
from ..endptscanner import BpipeEndpointSniffer
from ..messagebus import BpipeEndPointListWriter

@dataclass
class AWSAdapter():
    bpipeEndPointSniffer: BpipeEndpointSniffer
    bpipeEndPointListWriter: BpipeEndPointListWriter


def aws_service_factory(topicARN:str) -> AWSAdapter:
    bpipeEndPointSniffer = PrivateLinkBpipeEndpointSniffer()
    bpipeEndPointListWriter = SNSBpipeEndPointListWriter(topicARN)
    return AWSAdapter(
        bpipeEndPointSniffer, bpipeEndPointListWriter
    )



