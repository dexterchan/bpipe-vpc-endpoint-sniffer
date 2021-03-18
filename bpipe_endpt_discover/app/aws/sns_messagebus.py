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



"""
    AWS Implementation class of BpipeEndPointListWriter with SNS
    1) boostrap the final message to BPIPE canary
    2) publish message to SNS channel
"""
class SNSBpipeEndPointListWriter(BpipeEndPointListWriter):
    def __init__(self, TopicArn: str) -> None:
        self.client = boto3.client('sns')
        self.topicArn = TopicArn
        self.batch_size = 50
        self.rest_time_second = 0.5
    @staticmethod
    def __batch_convert(bpipeLst:List[Dict], n:int):
        """
            batching the message sending to SNS to avoid throttling
            do the final conversion to meet final format to SNS channel
        """
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
        
        # from https://docs.aws.amazon.com/general/latest/gr/sns.html
        # sns publish quota limit is 300 transactin per second
        # to avoid throttling, we limit 50 per batch
        for sublst in self.__batch_convert(newlst, self.batch_size):
            try:
                for msg in sublst:
                    self._send_msg_To_SNS_helper(msg)
            except Exception as e:
                logger.error(e)
                raise e
            time.sleep(self.rest_time_second)
    
    def _send_msg_To_SNS_helper(self, msg: Dict):
        """
            call SNS API publish
        """
        jsonStr = json.dumps(msg)
        logger.debug(f"attempt writing to SNS:{jsonStr}")
        response = self.client.publish(
            TopicArn = self.topicArn,
            Message = jsonStr,
            MessageStructure='json'
        )
        msg_id = response.get("MessageId", "")
        logger.info(f"writing to SNS {msg_id}:{jsonStr}")
