from tests.conftest import MockBpipeEndPointListWriter
from bpipe_endpt_sniffer.app.setting import ProbeSetting, IncomingRequest
import os
from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer
from bpipe_endpt_sniffer.app.messagebus import BpipeEndPointListWriter

import json
from typing import cast

import pytest

SAMPLE_SIZE = 100
def test_sniff_endpoint(getSampleInput:IncomingRequest,endpoint_sniffer:BpipeEndpointSniffer):
     endpointTag = getSampleInput.sniff_tags
     endpointlst = endpoint_sniffer.sniff_bpipe_endpoints(endpointTag)
     assert  len(endpointlst) == SAMPLE_SIZE

def test_lambda_handler(getSampleInput:IncomingRequest, endpoint_sniffer:BpipeEndpointSniffer, 
     bpipeEndPointListWriter:BpipeEndPointListWriter):
    assert getSampleInput is not None
   
    assert getSampleInput.probe.testTicker == "BBHBEAT Index"
    endpointTag = getSampleInput.sniff_tags
    endpointlst = endpoint_sniffer.sniff_bpipe_endpoints(endpointTag)

    bpipeEndPointListWriter.write_BpipeEndpoint_list_to_messagebus(
         incomingRequest= getSampleInput,
         bpipeEndpointLst= endpointlst
    )
    mockbpipeEndPointListWriter = cast (MockBpipeEndPointListWriter, bpipeEndPointListWriter)
    assert len(mockbpipeEndPointListWriter.outputBuffer) == SAMPLE_SIZE
    for eventstr in mockbpipeEndPointListWriter.outputBuffer:
         obj = json.loads(eventstr)
         msg = json.loads (obj["MessageBody"])
         hostname = msg["detail"]["hostname"]
         id = msg["detail"]["id"]
         assert hostname is not None
         assert id is not None







