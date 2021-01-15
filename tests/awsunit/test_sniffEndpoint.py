from bpipe_endpt_discover.app.endptscanner import BpipeEndpointDiscover
from bpipe_endpt_discover.app.setting import ProbeSetting, IncomingRequest
from bpipe_endpt_discover.app.aws.setup import aws_service_factory

import os
import boto3
import logging
boto3.set_stream_logger("boto3", logging.ERROR)
boto3.set_stream_logger("botocore", logging.ERROR)

os.environ["SQS_URL"] = "https://sqs.us-east-1.amazonaws.com/191791126208/csa-healthcheck-bpipe-endpoint"
os.environ["SNS_ARN"] = "arn:aws:sns:us-east-1:191791126208:bpipe-publish-endpoint-to-canary"
def test_discover_bpipe_endpoints(getSampleInput:IncomingRequest):
    awsAdapter = aws_service_factory(os.environ["SNS_ARN"])
    endpointTag = getSampleInput.discover_tags
    discover:BpipeEndpointDiscover = None
    discover, writer = (awsAdapter.bpipeEndPointDiscover,
                        awsAdapter.bpipeEndPointListWriter)
    endpointLst =  discover.discover_bpipe_endpoints(
        endpointTag
     )
    assert len(endpointLst) == 2
    writer.write_bpipeendpoint_list_to_messagebus(getSampleInput, endpointLst)
    

