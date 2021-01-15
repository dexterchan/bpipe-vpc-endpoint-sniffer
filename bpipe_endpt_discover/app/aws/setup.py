
from dataclasses import dataclass
from .privateLink import PrivateLinkBpipeEndpointSniffer
#from .sqs_messagebus import SQSBpipeEndPointListWriter
from .sns_messagebus import SNSBpipeEndPointListWriter
from ..endptscanner import BpipeEndpointSniffer
from ..messagebus import BpipeEndPointListWriter
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

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



