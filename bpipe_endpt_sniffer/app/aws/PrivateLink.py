import boto3
from ..model import BpipeEndpoint, BpipeFeature
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PrivateLinkBpipeEndpointSniffer:
    def __init__(self) -> None:
        self.client = boto3.client('ec2')

    def sniff_bpipe_endpoints(self, bpipeFeature:BpipeFeature)->List[BpipeEndpoint]:
        logger.debug(bpipeFeature)
        bpipeEndpointLst:List[BpipeEndpoint] = []

        try:
            response = self.__sniff_vpcendpoint_helper(bpipeFeature, False)
            #Get DNS entries
            #Get ID
            if "VpcEndpoints" not in response:
                raise Exception("Not vpc endpoint found!")
            vpcendpointlst = response["VpcEndpoints"]
            logging.info(f"Found {len(vpcendpointlst)} active bpipe endpoints")

            for endpt in vpcendpointlst:
                hostname = endpt["DnsEntries"][0]["DnsName"]
                nametaglst = list(filter( lambda tag: tag["Key"] == "Name",endpt["Tags"]))
                name = nametaglst[0]["Value"]
                logging.info(f"{name}:{hostname}")
                bpipeEndpointLst.append(
                    BpipeEndpoint(
                        hostname = hostname,
                        bpipe_id = name
                    )
                )


        except Exception as err:
            logger.error(err)
        return bpipeEndpointLst


    def __sniff_vpcendpoint_helper(self, bpipeFeature:BpipeFeature, dryRun:bool)->Dict:
        response = self.client.describe_vpc_endpoints(
                DryRun=False,
                Filters=[
                    {
                        'Name': 'vpc-endpoint-type',
                        'Values': [
                            'Interface',
                        ]
                    },
                    {
                        'Name': 'tag:BusinessUnit',
                        'Values':[bpipeFeature.BusinessUnit]
                    },
                    {
                        'Name': 'tag:Environment',
                        'Values' : [bpipeFeature.Environment]
                    },
                    {
                        'Name': 'vpc-endpoint-state',
                        'Values':["available"]
                    },
                    {
                        'Name': 'tag-key',
                        'Values':["Name"]
                    }
                ]
            )
        return response