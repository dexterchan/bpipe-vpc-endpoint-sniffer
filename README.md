# bpipe-vpc-endpoint-discover

bpipe-vpc-endpoint-discover is a small compute function searching all existing interface endpoints in an account.  
AWS: In a regulatar time internval, Eventbridge triggers this endpoint-discover to search for all eligible vpc endpoint for health checking by bpipe-canary lambda.

It will filter the interface endpoints by tags specified in Eventbridge input event. 
The workflow is documented in [Architecture diagram](https://cms.prod.bloomberg.com/team/display/~calbert3/CSA+-+B-PIPE+Canary+implementation)  
The input of the searching tag is "discover_tags" field in the input json.  
The input also specify the bpipe Canary input template in "probe" field.  
```
{
  "region": "us-east-1",
  "provider" : "aws",
  "probe": {
    "port": "8194",
    "authAppCredential": "EDC:Canary-QA",
    "testTicker": "BBHBEAT Index",
    "expectedTickers": "58",
    "max_run_seconds": "60"
  },
  "discover_tags":{
    "BusinessUnit": "ed-cloud-solutions",
    "Environment": "qa"
  }
}
```
After finding the interface endpoints, it will insert vpc address and "Name" tag values into the "probe".  
Finally it boostraps the input event of bpipe canary and publish into SNS. SNS will trigger Bpipe Canary lambda for health checking.  

```
{
            "region": <region>,
            "provider": <cloud vendor>,
            "detail": {
                <fields derived from input event json message field probe>,
                <fields from bpipe endpoint: hostname and name tag of vpc endpoint>
            }
}
```


## Build with sam
To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

## Build and package with zip

```bash
make package
```


Run functions locally and invoke them with the `sam local invoke` command.

```bash
bpipe-vpc-endpoint-discover$ sam local invoke BPipeEndPointDiscoverFunction --event events/event.json
```

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests.

```bash
export PYTHONPATH=$(pwd)/bpipe_endpt_discover
bpipe-vpc-endpoint-discover$ pip install pytest pytest-mock --user
bpipe-vpc-endpoint-discover$ python -m pytest tests/ -s
```


## Upload Package for deployment
Re-open the VS-Code as local mode and run `make upload s3prefix=${S3_URI}`. This will build, package and upload the function and the layer to S3 under th provided prefix.

