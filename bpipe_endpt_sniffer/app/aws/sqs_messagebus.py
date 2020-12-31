from typing import List
from ..model import BpipeEndpoint
import boto3
import logging

logger = logging.getLogger(__name__)

class SQSBpipeEndPointListWriter:
    def __init__(self, queueURL: str) -> None:
        self.client = boto3.client('sqs')
    def write_BpipeEndpoint_list_to_messagebus(self, bpipeEndpointLst:List[BpipeEndpoint])->None:
        return NotImplementedError("Not implemented")