from tests.conftest import MockBpipeEndPointListWriter
from bpipe_endpt_discover.app.setting import ProbeSetting, IncomingRequest
import os
from bpipe_endpt_discover.app.endptscanner import BpipeEndpointDiscover
from bpipe_endpt_discover.app.messagebus import BpipeEndPointListWriter

import json
from typing import cast

import pytest

SAMPLE_SIZE = 100
def test_discover_endpoint(getSampleInput:IncomingRequest,endpoint_discover:BpipeEndpointDiscover):
     """
          test the discover endpoint scanning with the given mock input event
     """
     
     endpointTag = getSampleInput.discover_tags
     endpointlst = endpoint_discover.discover_bpipe_endpoints(endpointTag)
     assert  len(endpointlst) == SAMPLE_SIZE

def test_lambda_handler(getSampleInput:IncomingRequest, endpoint_discover:BpipeEndpointDiscover, 
     bpipeEndPointListWriter:BpipeEndPointListWriter):
    """
          test the discover endpoint scanning with the given mock input event
          test the final message output from BpipeEndPointListWriter
     """
    assert getSampleInput is not None
   
    assert getSampleInput.probe.testTicker == "BBHBEAT Index"
    endpointTag = getSampleInput.discover_tags
    endpointlst = endpoint_discover.discover_bpipe_endpoints(endpointTag)

    bpipeEndPointListWriter.write_bpipeendpoint_list_to_messagebus(
         incomingRequest= getSampleInput,
         bpipeEndpointLst= endpointlst
    )
    mockbpipeEndPointListWriter = cast (MockBpipeEndPointListWriter, bpipeEndPointListWriter)
    assert len(mockbpipeEndPointListWriter.outputBuffer) == SAMPLE_SIZE
    cnt = 0
    for eventstr in mockbpipeEndPointListWriter.outputBuffer:
         obj = json.loads(eventstr)
         msg = json.loads (obj["MessageBody"])
         hostname = msg["detail"]["hostname"]
         id = msg["detail"]["id"]
         assert hostname == f"test{cnt}"
         assert id == f"bpipe{cnt}"
         assert getSampleInput.probe.testTicker == msg["detail"]["testTicker"]
         assert getSampleInput.probe.expectedTickers == msg["detail"]["expectedTickers"]
         print (hostname + " " + id)
         cnt = cnt + 1







