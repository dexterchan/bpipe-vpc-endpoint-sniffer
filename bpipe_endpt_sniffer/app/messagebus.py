from __future__ import annotations
from typing import Protocol, List, Dict
from .model import BpipeEndpoint
from .setting import IncomingRequest
import copy
class BpipeEndPointListWriter(Protocol):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def __convertDict(self, template:Dict, bpipeEndpt: BpipeEndpoint)->Dict:
        dataDict = copy.deepcopy(template)
        dataDict["detail"]["hostname"] = bpipeEndpt.hostname
        dataDict["detail"]["id"] = bpipeEndpt.bpipe_id
        return dataDict

    def convertFormat(self, incomingRequest:IncomingRequest, bpipeEndpointLst:List[BpipeEndpoint])-> List[Dict]:
        output_template_Dict = incomingRequest.write_OutputTemplate()
        newlst = list(map(lambda endpt: self.__convertDict(output_template_Dict, endpt), bpipeEndpointLst))
        return newlst

    def write_BpipeEndpoint_list_to_messagebus(self, 
        incomingRequest:IncomingRequest, 
        bpipeEndpointLst:List[BpipeEndpoint])->None:
        ...

