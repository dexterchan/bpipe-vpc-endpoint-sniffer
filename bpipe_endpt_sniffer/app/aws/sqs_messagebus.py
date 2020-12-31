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
    def __chunkConvert(bpipeLst:List[BpipeEndpoint], pointer:int, n:int) -> List[Dict]:
        sublst = bpipeLst[pointer: pointer+n]
        mList = list(map(
                lambda endpt : {
                    "Id": str(uuid.uuid4()),
                    "MessageBody": json.dumps(endpt)
                }
                ,sublst
            ))
        return (mList, pointer + n)

    def write_BpipeEndpoint_list_to_messagebus(self, incomingRequest:IncomingRequest,bpipeEndpointLst:List[BpipeEndpoint])->None:
        #Prepare the format first
        newlst = super().convertFormat(
            incomingRequest = incomingRequest,
            bpipeEndpointLst = bpipeEndpointLst
            )
        sublst = None
        pointer = 0
        while True:
            sublst, pointer = self.__chunkConvert(newlst, pointer, self.batch_size)
            if len(sublst) == 0:
                break
            self.__send_msg_To_SQS_helper(msgList = sublst)
        
    #Sending by chunk to avoid throttling!!!
    def __send_msg_To_SQS_helper(self, msgList: List[Dict]):
        self.client.send_message_batch(
            QueueUrl = self.sqsURL,
            Entries = msgList
        )