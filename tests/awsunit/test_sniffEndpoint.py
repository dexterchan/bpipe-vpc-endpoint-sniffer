from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer, BpipeFeature
from bpipe_endpt_sniffer.app.aws.setup import aws_service_factory

import os
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

os.environ["SQS_URL"] = "arn:aws:sqs:us-east-1:191791126208:csa-healthcheck-bpipe-endpoint"

def test_aws_service_factory():
    awsAdapter = aws_service_factory(os.environ["SQS_URL"])
    bpipeFeature = BpipeFeature(
         BusinessUnit = os.environ["BusinessUnit"],
         Environment = os.environ["Environment"]
     )
    endpointLst = awsAdapter.bpipeEndPointSniffer.sniff_bpipe_endpoints(
        bpipeFeature
     )
    assert len(endpointLst) == 2



