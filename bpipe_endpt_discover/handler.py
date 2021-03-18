import json
import os

from app.aws.setup import aws_service_factory
from app.endptscanner import BpipeEndpointDiscover
from app.messagebus import BpipeEndPointListWriter
from app.model import BpipeEndpoint
from app.setting import IncomingRequest
from app.logging import get_logger
SNS_ARN = os.environ["SNS_ARN"]
logger = get_logger(__name__)

awsAdapter = aws_service_factory(SNS_ARN)


def lambda_handler(event, context):
    """entry point of lambda function.

    1) initialize the cloud provider service for 
    a) BpipeEndpointDiscover - end point searching for interface end point
    b) bpipeEndPointListWriter - massage endpoint info and publish to data bus
    2) massage the end point information to Bpipe Canary input
    3) publish the bpipe canary input event to SNS to trigger Bpipe Canary lambda

    Args:
        event: the input event from AWS EventBridge scheduler.
        Format was inherited from AWS Event

    Returns:
        List of dict of BpipeEndpoint
    """
    incoming_request = IncomingRequest.from_request(event)

    endpointTag = event["discover_tags"]
    discover, writer = (awsAdapter.bpipeEndPointDiscover,
                       awsAdapter.bpipeEndPointListWriter)
    endpointLst = discover.discover_bpipe_endpoints(
        endpointTag
    )

    output_lst = [endPt.dict() for endPt in endpointLst]
    logger.info(f"Endpts:{str(output_lst)}")
    writer.write_bpipeendpoint_list_to_messagebus(incoming_request, endpointLst)

    return output_lst
