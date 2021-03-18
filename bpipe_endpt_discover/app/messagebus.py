from __future__ import annotations
from typing import List, Dict
from abc import abstractmethod, ABC
from .model import BpipeEndpoint
from .setting import IncomingRequest
import copy
class BpipeEndPointListWriter(ABC):
    """
        Interface to massage endpoint info to Bpipe Canary readable format
        finally, it writes into data bus to trigger Bpipe canary lambda

        final output format:
        {
            "region": <region>,
            "provider": <cloud vendor>,
            "detail": {
                <fields derived from input event json message field probe>,
                <fields from bpipe endpoint: hostname and name tag of vpc endpoint>
            }
        }
    """
    def _convert_dict(self, template:Dict, bpipeEndpt: BpipeEndpoint)->Dict:
        """
            inject bpipe vpc endpoint info into the "Bpipe discover input event 
            json message field: "probe"
        """
        dataDict = copy.deepcopy(template)
        dataDict["detail"]["hostname"] = bpipeEndpt.hostname
        dataDict["detail"]["id"] = bpipeEndpt.bpipe_id
        return dataDict

    def convert_format(self, incomingRequest:IncomingRequest, bpipeEndpointLst:List[BpipeEndpoint])-> List[Dict]:
        """
         massage function to help boostrap the Bpipe Canary input mesasge from
         1) Bpipe discover input event json message field: "probe"
         2) vpc endpoint information : name and address
        """
        output_template_dict = incomingRequest.write_output_template()
        newlst = [self._convert_dict(output_template_dict, endpt) for endpt in bpipeEndpointLst]

        return newlst

    @abstractmethod
    def write_bpipeendpoint_list_to_messagebus(self,
                                               incomingRequest:IncomingRequest,
                                               bpipeEndpointLst:List[BpipeEndpoint])->None:
        ...

