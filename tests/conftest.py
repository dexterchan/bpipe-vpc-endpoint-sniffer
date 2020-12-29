import pytest
from bpipe_endpt_sniffer.app.endptscanner import BpipeEndpointSniffer
from bpipe_endpt_sniffer.app.aws.PrivateLink import PrivateLinkBpipeEndpointSniffer

@pytest.fixture
def endpoint_sniffer() -> BpipeEndpointSniffer:
    return PrivateLinkBpipeEndpointSniffer()