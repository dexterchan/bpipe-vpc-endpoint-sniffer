# bpipe-vpc-endpoint-discover

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
bpipe-vpc-endpoint-discover$ python -m pytest tests/ -v
```


## Upload Package for deployment
Re-open the VS-Code as local mode and run `make upload s3prefix=${S3_URI}`. This will build, package and upload the function and the layer to S3 under th provided prefix.

