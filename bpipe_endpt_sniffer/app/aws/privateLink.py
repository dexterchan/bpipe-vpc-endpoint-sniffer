import boto3
from ..model import BpipeEndpoint
from typing import List, Dict
import logging
import copy
import json
logger = logging.getLogger(__name__)

class PrivateLinkBpipeEndpointSniffer:
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

    def sniff_bpipe_endpoints(self, bpipeTags:Dict)->List[BpipeEndpoint]:
        #Prepare sniffer scope
        sniff_scope_list= self.__fill_in_sniffer_scope(bpipeTags)
        logger.info(f"Sniff scope:{json.dumps(sniff_scope_list)}")
        bpipeEndpointLst:List[BpipeEndpoint] = []

        try:
            response = self.__sniff_vpcendpoint_helper(sniff_scope_list, False)
            #Get DNS entries
            #Get ID
            if "VpcEndpoints" not in response:
                raise Exception("Not vpc endpoint found!")
            vpcendpointlst = response["VpcEndpoints"]
            logger.info(f"Found {len(vpcendpointlst)} active bpipe endpoints")

            for endpt in vpcendpointlst:
                hostname = endpt["DnsEntries"][0]["DnsName"]
                nametaglst = list(filter( lambda tag: tag["Key"] == "Name",endpt["Tags"]))
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

    def __fill_in_sniffer_scope(self, sniffTags:Dict) -> List[Dict]:
        sniffTagLst = copy.deepcopy(self.baseField)
        for key, value in sniffTags.items():
            sniffTagLst.append(
                {
                    'Name': f'tag:{key}',
                    'Values':[ value ]
                }
            )
        return sniffTagLst
    def __sniff_vpcendpoint_helper(self, sniff_scope:List[Dict], dryRun:bool)->Dict:
        response = self.client.describe_vpc_endpoints(
                DryRun = False,
                Filters = sniff_scope
            )
        return response