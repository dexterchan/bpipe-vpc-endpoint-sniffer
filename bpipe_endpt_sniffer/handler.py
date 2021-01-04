import json
import os

from app.aws.setup import aws_service_factory
from app.endptscanner import BpipeEndpointSniffer
from app.messagebus import BpipeEndPointListWriter
from app.model import BpipeEndpoint
from app.setting import IncomingRequest
from app.logging import get_logger
SNS_ARN = os.environ["SNS_ARN"]
logger = get_logger(__name__)

awsAdapter = aws_service_factory(SNS_ARN)


def lambda_handler(event, context):
    incoming_request = IncomingRequest.from_request(event)

    endpointTag = event["sniff_tags"]
    sniffer: BpipeEndpointSniffer = None
    writer: BpipeEndPointListWriter = None
    sniffer, writer = (awsAdapter.bpipeEndPointSniffer,
                       awsAdapter.bpipeEndPointListWriter)
    endpointLst = sniffer.sniff_bpipe_endpoints(
        endpointTag
    )

    output_lst = []
    for endPt in endpointLst:
        output_lst.append(endPt.dict())
    logger.info(f"Endpts:{str(output_lst)}")
    writer.write_bpipeendpoint_list_to_messagebus(incoming_request, endpointLst)

    return output_lst
