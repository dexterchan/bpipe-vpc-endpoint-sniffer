from __future__ import annotations
from typing import List, Dict
from abc import abstractmethod, ABC
from .model import BpipeEndpoint
from .setting import IncomingRequest
import copy
class BpipeEndPointListWriter(ABC):
    """
        Sniff all bpipe endpoint in an environment for next processing
    """
    def _convert_dict(self, template:Dict, bpipeEndpt: BpipeEndpoint)->Dict:
        dataDict = copy.deepcopy(template)
        dataDict["detail"]["hostname"] = bpipeEndpt.hostname
        dataDict["detail"]["id"] = bpipeEndpt.bpipe_id
        return dataDict

    def convert_format(self, incomingRequest:IncomingRequest, bpipeEndpointLst:List[BpipeEndpoint])-> List[Dict]:
        output_template_dict = incomingRequest.write_output_template()
        newlst = [self._convert_dict(output_template_dict, endpt) for endpt in bpipeEndpointLst]

        return newlst

    @abstractmethod
    def write_bpipeendpoint_list_to_messagebus(self,
                                               incomingRequest:IncomingRequest,
                                               bpipeEndpointLst:List[BpipeEndpoint])->None:
        ...

