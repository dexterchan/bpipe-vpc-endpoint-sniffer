import pytest
import os
import json
os.environ["SQS_URL"] = "https://sqs.us-east-1.amazonaws.com/191791126208/csa-healthcheck-bpipe-endpoint"
os.environ["SNS_ARN"] = "arn:aws:sns:us-east-1:191791126208:bpipe-publish-endpoint-to-canary"

from bpipe_endpt_discover import handler
from bpipe_endpt_discover.app.setting import IncomingRequest


@pytest.fixture
def get_json_input() -> IncomingRequest:
    with open("events/event.json", "r") as f:
        data = json.load(f)
    assert data is not None

    return data

def test_discover_bpipe_endpoints_with_handler(get_json_input:dict):
    handler.lambda_handler(get_json_input, None)
