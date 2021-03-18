
from dataclasses import dataclass
from .privateLink import PrivateLinkBpipeEndpointDiscover
#from .sqs_messagebus import SQSBpipeEndPointListWriter
from .sns_messagebus import SNSBpipeEndPointListWriter
from ..endptscanner import BpipeEndpointDiscover
from ..messagebus import BpipeEndPointListWriter
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

@dataclass
class AWSAdapter():
    """ container class of service instance
    """
    bpipeEndPointDiscover: BpipeEndpointDiscover
    bpipeEndPointListWriter: BpipeEndPointListWriter


def aws_service_factory(topicARN:str) -> AWSAdapter:
    """Prepares all the AWS dependencies of the application. Call in your main and pass the relevant services to the core domain of the app.

    Returns:
        AWSAdapters: the aws dependencies.
    """
    bpipeEndPointDiscover = PrivateLinkBpipeEndpointDiscover()
    bpipeEndPointListWriter = SNSBpipeEndPointListWriter(topicARN)
    return AWSAdapter(
        bpipeEndPointDiscover, bpipeEndPointListWriter
    )



