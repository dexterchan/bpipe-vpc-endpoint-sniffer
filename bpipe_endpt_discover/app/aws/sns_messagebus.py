from typing import List
from ..model import BpipeEndpoint
from ..setting import IncomingRequest
from ..messagebus import BpipeEndPointListWriter
import boto3
import logging
import uuid
import json
from typing import Dict, Optional
import time
logger = logging.getLogger(__name__)

# from https://docs.aws.amazon.com/general/latest/gr/sns.html
# sns publish quota limit is 300 transactin per second
# to avoid throttling, we limit 50 per batch

class SNSBpipeEndPointListWriter(BpipeEndPointListWriter):
    def __init__(self, TopicArn: str) -> None:
        self.client = boto3.client('sns')
        self.topicArn = TopicArn
        self.batch_size = 50
        self.rest_time_second = 0.5
    @staticmethod
    def _branch_convert(bpipeLst:List[BpipeEndpoint], n:int):
        for i in range (0, len(bpipeLst), n):
            sublst = bpipeLst[i:i+n]
            mList = [{"default": json.dumps(endpt)} for endpt in sublst]
            yield mList

    def write_bpipeendpoint_list_to_messagebus(self, incomingRequest:IncomingRequest, bpipeEndpointLst:List[BpipeEndpoint])->None:
        #Prepare the format first
        newlst = self.convert_format(
            incomingRequest=incomingRequest,
            bpipeEndpointLst=bpipeEndpointLst
            )
        sublst = None
        
        for sublst in self._branch_convert(newlst, self.batch_size):
            try:
                for msg in sublst:
                    self._send_msg_To_SNS_helper(msg)
            except Exception as e:
                logger.error(e)
                raise e
            time.sleep(self.rest_time_second)
    
    def _send_msg_To_SNS_helper(self, msg: Dict):
        jsonStr = json.dumps(msg)
        logger.debug(f"attempt writing to SNS:{jsonStr}")
        response = self.client.publish(
            TopicArn = self.topicArn,
            Message = jsonStr,
            MessageStructure='json'
        )
        msg_id = response.get("MessageId", "")
        logger.info(f"writing to SNS {msg_id}:{jsonStr}")