# minimalistic utility to test and develop locally

SHELL = /bin/sh
.DEFAULT_GOAL := help

export DOCKER_IMAGE_NAME ?= jsonifier
export DOCKER_IMAGE_TAG ?= 1.0.2

export MASTER_AWS_REGISTRY ?= registry.osparc-master-zmt.click
export MASTER_REGISTRY ?= registry.osparc-master.speag.com
export STAGING_REGISTRY ?= registry.osparc.speag.com
export LOCAL_REGISTRY ?= registry:5000

define _bumpversion
	# upgrades as $(subst $(1),,$@) version, commits and tags
	@docker run --rm -v $(PWD):/${DOCKER_IMAGE_NAME} \
		-u $(shell id -u):$(shell id -g) \
		itisfoundation/ci-service-integration-library:latest \
		sh -c "cd /${DOCKER_IMAGE_NAME} && bump2version --verbose --list --config-file $(1) $(subst $(2),,$@)"
endef

.PHONY: version-patch version-minor version-major
version-patch version-minor version-major: .bumpversion.cfg ## increases service's version
	@make compose-spec
	@$(call _bumpversion,$<,version-)
	@make compose-spec

.PHONY: compose-spec
compose-spec: ## runs ooil to assemble the docker-compose.yml file
	@docker run --rm -v $(PWD):/${DOCKER_IMAGE_NAME} \
		-u $(shell id -u):$(shell id -g) \
		itisfoundation/ci-service-integration-library:latest \
		sh -c "cd /${DOCKER_IMAGE_NAME} && ooil compose"

clean:
	rm -rf docker-compose.yml
	rm -rf validation-tmp

add_metadata_inputs:
	cd helper_scripts && \
		pip install pyyaml && \
		python add_metadata_inputs.py ../.osparc/jsonifier/metadata.yml ../.osparc/jsonifier/metadata.yml

.PHONY: build
build: clean add_metadata_inputs compose-spec	## build docker image
	docker compose build

.PHONY: run-local
run-local: build	## runs image with local configuration
	docker compose down
	rm -rf validation-tmp
	cp -r validation validation-tmp
	docker compose --file docker-compose-local.yml up

.PHONY: publish-local
publish-local: ## push to local throw away registry to test integration
	docker tag simcore/services/comp/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} $(LOCAL_REGISTRY)/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	docker push registry:5000/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	@curl registry:5000/v2/_catalog | jq

.PHONY: publish-staging
publish-staging: run-local ## push to local throw away registry to test integration
	docker tag simcore/services/comp/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} $(STAGING_REGISTRY)/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	docker push $(STAGING_REGISTRY)/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

.PHONY: publish-master
publish-master: run-local ## push to local throw away registry to test integration
	docker tag simcore/services/comp/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} $(MASTER_REGISTRY)/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	docker push $(MASTER_REGISTRY)/simcore/services/comp/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

.PHONY: help
help: ## this colorful help
	@echo "Recipes for '$(notdir $(CURDIR))':"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
