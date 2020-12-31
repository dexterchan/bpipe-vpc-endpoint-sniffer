from typing import List
from ..model import BpipeEndpoint
from ..setting import IncomingRequest
import boto3
import logging
import uuid
import json
from typing import Dict
logger = logging.getLogger(__name__)

class SQSBpipeEndPointListWriter:
    def __init__(self, queueURL: str) -> None:
        self.client = boto3.client('sqs')
        self.sqsURL = queueURL
        self.batchSize = 10

    @staticmethod
    def __chunk(bpipeLst:List[BpipeEndpoint], n:int) -> List[Dict]:
        for i in range(0, len(bpipeLst), n):
            lst = bpipeLst[i : i + n]

            yield map(
                lambda endpt : {
                    "Id": str(uuid.uuid4()),
                    "MessageBody": json.dumps(endpt)
                }
                ,lst
            )

    def write_BpipeEndpoint_list_to_messagebus(self, incomingRequest:IncomingRequest,bpipeEndpointLst:List[BpipeEndpoint])->None:
        #Prepare the format first
        newlst = super().convertFormat(
            incomingRequest = incomingRequest,
            bpipeEndpointLst = bpipeEndpointLst
            )
        #Batch it properly later
        for bpipeEndpt in self.__chunk(newlst, self.batchSize):
            
        pass
        

    def __send_To_SQS_helper(self, bpipeEndPointLst: List[BpipeEndpoint]):
        

        pass