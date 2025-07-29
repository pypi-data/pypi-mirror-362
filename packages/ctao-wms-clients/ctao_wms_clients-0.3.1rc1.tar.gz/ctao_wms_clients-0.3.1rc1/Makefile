###
export CHART_NAME=wms
export CHART_LOCATION=chart
export DOCKER_IMAGE_CONTEXT=docker/client

include dpps-aiv-toolkit/Makefile


# TODO: move this to kit
export TEST_ARTIFACTS_PATH ?= $(PWD)
export TEST_REPORT_CONFIG ?= $(PWD)/aiv-config.yml
export TEX_CONTENT_PATH ?= $(PWD)/report



build-dev-server-images:
	docker build docker/client/ -t harbor.cta-observatory.org/dpps/wms-client:dev
	docker build docker/server/ -t harbor.cta-observatory.org/dpps/wms-server:dev
	docker build docker/ce/ -t harbor.cta-observatory.org/dpps/wms-ce:dev
	./kind -n kind-dpps-test-local load docker-image \
		harbor.cta-observatory.org/dpps/wms-client:dev \
		harbor.cta-observatory.org/dpps/wms-ce:dev \
		harbor.cta-observatory.org/dpps/wms-server:dev

dev: build-dev-server-images

.PHONY: build-dev-server-images
