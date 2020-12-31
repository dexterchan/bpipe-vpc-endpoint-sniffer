import pytest
from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer
from bpipe_endpt_sniffer.app.messagebus import BpipeEndPointListWriter

from bpipe_endpt_sniffer.app.model import BpipeEndpoint, BpipeFeature
from typing import List
import json

class MockBpipeEndpointSniffer:
    def sniff_bpipe_endpoints(self, bpipeFeature:BpipeFeature)->List[BpipeEndpoint]:
        numberOfEndpoint = 2
        bpipeEndptLst:List[BpipeEndpoint] = []
        for i in range(numberOfEndpoint):
            bpipeEndptLst.append(
                BpipeEndpoint(
                    hostname = f"test{str(i)}",
                    bpipe_id = f"bpipe{str(i)}"
                )
            )
        return bpipeEndptLst

class MockBpipeEndPointListWriter:
    def __init__(self) -> None:
        self.outputBuffer:List[str] = []
    def write_BpipeEndpoint_list_to_messagebus(self, bpipeEndpointLst:List[BpipeEndpoint])->None:
        for bpipeEndpt in bpipeEndpointLst:
            self.outputBuffer.append(json.dump(bpipeEndpt))

@pytest.fixture
def endpoint_sniffer() -> BpipeEndpointSniffer:
    return MockBpipeEndpointSniffer()

@pytest.fixture
def bpipeEndPointListWriter() -> BpipeEndPointListWriter:
    return MockBpipeEndPointListWriter()