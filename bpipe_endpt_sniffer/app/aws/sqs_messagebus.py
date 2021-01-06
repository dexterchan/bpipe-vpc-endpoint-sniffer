from typing import List
from ..model import BpipeEndpoint
from ..setting import IncomingRequest
from ..messagebus import BpipeEndPointListWriter
import boto3
import logging
import uuid
import json
from typing import Dict
logger = logging.getLogger(__name__)

class SQSBpipeEndPointListWriter(BpipeEndPointListWriter):
    def __init__(self, queueURL: str) -> None:
        self.client = boto3.client('sqs')
        self.sqsURL = queueURL
        self.batch_size = 10

    @staticmethod
    def _branchConvert(bpipeLst:List[BpipeEndpoint], n:int):
        for i in range (0, len(bpipeLst), n):
            sublst = bpipeLst[i:i+n]
            mList = [{
                        "Id": str(uuid.uuid4()),
                        "MessageBody": json.dumps(endpt)
                    } for endpt in sublst]
            yield mList

    def write_bpipeendpoint_list_to_messagebus(self, incomingRequest:IncomingRequest, bpipeEndpointLst:List[BpipeEndpoint])->None:
        #Prepare the format first
        newlst = self.convert_format(
            incomingRequest = incomingRequest,
            bpipeEndpointLst = bpipeEndpointLst
            )
        sublst = None
        
        for sublst in self._branchConvert(newlst, self.batch_size):
            logger.info(f"writing to SQS:{json.dumps(sublst)}")
            self._send_msg_To_sqs_helper(msgList=sublst)
        
    #Sending by chunk to avoid throttling!!!
    def _send_msg_To_sqs_helper(self, msgList: List[Dict]):
        self.client.send_message_batch(
            QueueUrl=self.sqsURL,
            Entries=msgList
        )