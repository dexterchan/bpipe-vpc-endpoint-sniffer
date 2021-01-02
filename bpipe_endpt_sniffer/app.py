import json
import os

from .app.aws.setup import aws_service_factory
from .app.endptscanner import BpipeEndpointSniffer
from .app.messagebus import BpipeEndPointListWriter

SNS_ARN = os.environ["SNS_ARN"]

awsAdapter = aws_service_factory(SNS_ARN)

def lambda_handler(event, context):
    
    endpointTag = event["sniff_tags"]
    sniffer:BpipeEndpointSniffer = None
    writer:BpipeEndPointListWriter = None
    sniffer, writer = (awsAdapter.bpipeEndPointSniffer,
                        awsAdapter.bpipeEndPointListWriter)
    endpointLst =  sniffer.sniff_bpipe_endpoints(
        endpointTag
     )
    
    writer.write_BpipeEndpoint_list_to_messagebus(event, endpointLst)

    return endpointLst
