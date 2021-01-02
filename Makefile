include .env

init:
	pip install --user -r requirements.txt

deploy: package upload

clean:
	rm -rf .aws-sam/*

build: clean
	sam build -u -p
	mkdir -p .aws-sam/packages

package: build package-BPipeEndPointSnifferFunction

package-%:
	pushd .aws-sam/build/$* > /dev/null \
		&& zip -rq $*.zip . \
		&& mv $*.zip ../../packages/$*-$$(md5 -q $*.zip).zip; \
		popd > /dev/null

upload:
	test $(s3-prefix) || (echo "ERROR: s3-prefix required"; exit 1)
	aws --profile blpsaml --region us-east-1 s3  cp --recursive .aws-sam/packages/ $(s3-prefix)

typecheck:
	mypy bpipe_endpt_sniffer/app/

test:
	pytest $(path)
