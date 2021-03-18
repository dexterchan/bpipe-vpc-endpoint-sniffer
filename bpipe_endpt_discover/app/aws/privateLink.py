import boto3
from ..model import BpipeEndpoint
from typing import List, Dict
import logging
import copy
import json
logger = logging.getLogger(__name__)

"""
    AWS Implementation class of BpipeEndpointDiscover
    Scan all eligible interface VPC endpoint specified by given tag
"""
class PrivateLinkBpipeEndpointDiscover:
    def __init__(self) -> None:
        self.client = boto3.client('ec2')
        self.baseField = [
                    {
                        'Name': 'vpc-endpoint-type',
                        'Values': [
                            'Interface',
                        ]
                    },
                    {
                        'Name': 'vpc-endpoint-state',
                        'Values':["available"]
                    },
                    {
                        'Name': 'tag-key',
                        'Values':["Name"]
                    }]

    def discover_bpipe_endpoints(self, bpipeTags:Dict)->List[BpipeEndpoint]:
        #Prepare discover scope
        discover_scope_list= self._fill_in_discover_scope(bpipeTags)
        logger.info(f"Discover scope:{json.dumps(discover_scope_list)}")
        bpipeEndpointLst:List[BpipeEndpoint] = []

        try:
            response = self._discover_vpcendpoint_helper(discover_scope_list)
            #Get DNS entries
            #Get ID
            if "VpcEndpoints" not in response:
                raise Exception("Not vpc endpoint found!")
            vpcendpointlst = response["VpcEndpoints"]
            logger.info(f"Found {len(vpcendpointlst)} active bpipe endpoints")

            for endpt in vpcendpointlst:
                hostname = endpt["DnsEntries"][0]["DnsName"]
                nametaglst = [ tag for tag in endpt["Tags"] if tag["Key"] == "Name"]
                name = nametaglst[0]["Value"]
                logger.info(f"{name}:{hostname}")
                bpipeEndpointLst.append(
                    BpipeEndpoint(
                        hostname = hostname,
                        bpipe_id = name
                    )
                )
        except Exception as err:
            logger.error(err)
        return bpipeEndpointLst

    def _fill_in_discover_scope(self, discoverTags:Dict) -> List[Dict]:
        """
            extract the tag values to feed AWS API for scanning interface vpc endpoint
            massage the format to fit AWS API
        """
        discoverTagLst = copy.deepcopy(self.baseField)
        for key, value in discoverTags.items():
            discoverTagLst.append(
                {
                    'Name': f'tag:{key}',
                    'Values':[ value ]
                }
            )
        return discoverTagLst
    def _discover_vpcendpoint_helper(self, discover_scope:List[Dict], dryRun:bool = False)->Dict:
        """
            call the AWS API to scan interface vpc endpoint
        """
        response = self.client.describe_vpc_endpoints(
                DryRun = dryRun,
                Filters = discover_scope
            )
        return response
