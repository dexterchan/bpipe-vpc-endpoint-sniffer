from bpipe_endpt_sniffer.app.setting import IncomingRequest,  ProbeSetting
import pytest
from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer
from bpipe_endpt_sniffer.app.messagebus import BpipeEndPointListWriter

from bpipe_endpt_sniffer.app.model import BpipeEndpoint
from typing import List, Dict
import json
import os
import uuid
import copy
SAMPLE_SIZE = 100
class MockBpipeEndpointSniffer :
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
    def sniff_bpipe_endpoints(self, endptTag:Dict)->List[BpipeEndpoint]:
        numberOfEndpoint = SAMPLE_SIZE
        bpipeEndptLst:List[BpipeEndpoint] = []

        sniffTagLst = copy.deepcopy(self.baseField)
        for key, value in endptTag.items():
            sniffTagLst.append(
                {
                    'Name': f'tag:{key}',
                    'Values':[ value ]
                }
            )
        assert len(sniffTagLst) == len(self.baseField) + len(endptTag)

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

    def write_BpipeEndpoint_list_to_messagebus(self, 
        incomingRequest:IncomingRequest, 
        bpipeEndpointLst:List[BpipeEndpoint])->None:
        newlst = super().convertFormat(
            incomingRequest ,
            bpipeEndpointLst 
            )
        sublst = None
        pointer = 0
        while True:
            sublst, pointer = self.__chunkConvert(newlst, pointer, self.batch_size)
            if len(sublst) == 0:
                break
            for msg in sublst:
                self.outputBuffer.append(json.dumps(msg))

@pytest.fixture
def endpoint_sniffer() -> BpipeEndpointSniffer:
    return MockBpipeEndpointSniffer()

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
    