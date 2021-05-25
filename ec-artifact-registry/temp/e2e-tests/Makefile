
# load variables from a .env file
ifeq (,$(wildcard ~/.env),)
include .env
export $(shell sed 's/=.*//' .env)
endif

CLEAN_TARGETS = package .coverage dist venv .venv .pytest_cache dir_hash_zip *.zip

current_dir := $(shell pwd)

deploy_environment := $(if $(strip $(DEPLOY_ENVIRONMENT)),$(DEPLOY_ENVIRONMENT),$(shell git tag --sort version:refname | tail -1))

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d

check:
	pipenv check

sync:
	pipenv sync

.PHONY:
test: test-lambda test-api-gateway test-route53

.PHONY:
test-lambda:
	export DEPLOY_ENVIRONMENT=$(deploy_environment); \
	pipenv run pytest -s -vvv  tests/lambda

.PHONY:
test-api-gateway:
	export DEPLOY_ENVIRONMENT=$(deploy_environment); \
	pipenv run pytest -s -vvv  tests/api_gateway

.PHONY:
test-route53:
	export DEPLOY_ENVIRONMENT=$(deploy_environment); \
	pipenv run pytest -s -vvv  tests/route_53

test-cov:
	export DEPLOY_ENVIRONMENT=$(deploy_environment); \
	pipenv run pytest --cov=src --cov-report=term --cov-report=xml:cov.xml tests

pipenv-clean:
	pipenv clean

pipenv-lock:
	pipenv lock

pipenv-sync:
	pipenv sync

pipenv-update:
	pipenv update

pipenv-check:
	pipenv check

clean:
	for target in $(CLEAN_TARGETS); do \
		find . -name $$target -delete; \
	done

install:
	@echo installing package: $(package)
	pipenv install $(package)

install-dev:
	@echo installing package: $(package)
	pipenv install $(package) --dev
