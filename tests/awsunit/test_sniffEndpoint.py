from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer, BpipeFeature
from bpipe_endpt_sniffer.app.aws.setup import aws_service_factory
import os
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

os.environ["BusinessUnit"] = "ed-cloud-solutions"
os.environ["Environment"] = "qa"
def test_sniff_endpoint(endpoint_sniffer):
     bpipeFeature = BpipeFeature(
         BusinessUnit = os.environ["BusinessUnit"],
         Environment = os.environ["Environment"]
     )
     endpointlst = endpoint_sniffer.sniff_bpipe_endpoints(bpipeFeature)
     assert  len(endpointlst) == 2

def test_aws_service_factory():
    awsAdapter = aws_service_factory("testURL")
    bpipeFeature = BpipeFeature(
         BusinessUnit = os.environ["BusinessUnit"],
         Environment = os.environ["Environment"]
     )
    endpointLst = awsAdapter.bpipeEndPointSniffer.sniff_bpipe_endpoints(
        bpipeFeature
     )
    assert len(endpointLst) == 2