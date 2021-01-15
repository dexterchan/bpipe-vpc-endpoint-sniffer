from bpipe_endpt_discover.app.setting import IncomingRequest,  ProbeSetting
import pytest
from bpipe_endpt_discover.app.endptscanner import BpipeEndpointDiscover
from bpipe_endpt_discover.app.messagebus import BpipeEndPointListWriter

from bpipe_endpt_discover.app.model import BpipeEndpoint
from typing import List, Dict
import json
import os
import uuid
import copy
SAMPLE_SIZE = 100
class MockBpipeEndpointDiscover :
    def __init__(self) -> None:
        self.baseField = [
                    {
                        'Name': 'vpc-endpoint-type',
                        'Values': [
                            'Interface',
                        ]
                    },
                    {
                        'Name': 'vpc-endpoint-state',
                        'Values':["available"]
                    },
                    {
                        'Name': 'tag-key',
                        'Values':["Name"]
                    }]
    def discover_bpipe_endpoints(self, endptTag:Dict)->List[BpipeEndpoint]:
        numberOfEndpoint = SAMPLE_SIZE
        bpipeEndptLst:List[BpipeEndpoint] = []

        discoverTagLst = copy.deepcopy(self.baseField)
        for key, value in endptTag.items():
            discoverTagLst.append(
                {
                    'Name': f'tag:{key}',
                    'Values':[ value ]
                }
            )
        assert len(discoverTagLst) == len(self.baseField) + len(endptTag)

        for i in range(numberOfEndpoint):
            bpipeEndptLst.append(
                BpipeEndpoint(
                    hostname = f"test{str(i)}",
                    bpipe_id = f"bpipe{str(i)}"
                )
            )
        return bpipeEndptLst

class MockBpipeEndPointListWriter(BpipeEndPointListWriter):
    def __init__(self) -> None:
        self.outputBuffer:List[str] = []
        self.batch_size = 10
        
    @staticmethod
    def __branchConvert(bpipeLst:List[BpipeEndpoint], n:int):
        for i in range (0, len(bpipeLst), n):
            sublst = bpipeLst[i:i+n]
            mList = list(map(
                    lambda endpt : {
                        "Id": str(uuid.uuid4()),
                        "MessageBody": json.dumps(endpt)
                    }
                    ,sublst
                ))
            yield mList
    
    def write_bpipeendpoint_list_to_messagebus(self,
                                               incomingRequest:IncomingRequest,
                                               bpipeEndpointLst:List[BpipeEndpoint])->None:
        newlst = super().convert_format(
            incomingRequest ,
            bpipeEndpointLst 
            )
        sublst = None
        for sublst in self.__branchConvert(newlst, self.batch_size):
            for msg in sublst:
                self.outputBuffer.append(json.dumps(msg))

@pytest.fixture
def endpoint_discover() -> BpipeEndpointDiscover:
    return MockBpipeEndpointDiscover()

@pytest.fixture
def bpipeEndPointListWriter() -> BpipeEndPointListWriter:
    return MockBpipeEndPointListWriter()

@pytest.fixture
def getSampleInput() -> IncomingRequest:
    with open("events/event.json", "r") as f:
        data = json.load(f)
    assert data is not None
    probe = ProbeSetting(**data["probe"])
    return IncomingRequest.from_request(data)
    
