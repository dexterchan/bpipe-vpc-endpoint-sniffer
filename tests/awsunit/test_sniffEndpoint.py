from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer, BpipeFeature
from bpipe_endpt_sniffer.app.setting import ProbeSetting, IncomingRequest
from bpipe_endpt_sniffer.app.aws.setup import aws_service_factory

import os
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

os.environ["SQS_URL"] = "https://sqs.us-east-1.amazonaws.com/191791126208/csa-healthcheck-bpipe-endpoint"

def test_sniff_bpipe_endpoints(getSampleInput:IncomingRequest):
    awsAdapter = aws_service_factory(os.environ["SQS_URL"])
    bpipeFeature = BpipeFeature(
         BusinessUnit = getSampleInput.sniff_tags["BusinessUnit"],
         Environment = getSampleInput.sniff_tags["Environment"]
     )
    sniffer:BpipeEndpointSniffer = None
    sniffer, writer = (awsAdapter.bpipeEndPointSniffer,
                        awsAdapter.bpipeEndPointListWriter)
    endpointLst =  sniffer.sniff_bpipe_endpoints(
        bpipeFeature
     )
    assert len(endpointLst) == 2
    writer.write_BpipeEndpoint_list_to_messagebus(getSampleInput, endpointLst)
    

