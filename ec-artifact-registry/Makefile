
ifeq ($(shell test -e .env && echo -n yes),yes)
include .env
export $(shell sed 's/=.*//' .env)
endif

.EXPORT_ALL_VARIABLES:

BUILD_DIRS = artifacts_service deployment_service shared/code e2e-tests
DIRS_WITH_TESTS := $(shell ls -d *_lambda shared/code)
DIRS_WITH_TESTS += shared/code

all: copy-makefile clean setup-env test

.PHONY:
test-env:
	@env

.PHONY:
release: 
	@docker run --rm \
		-v $$PWD:/src \
		-e GIT_CREDENTIALS=$(GIT_CREDENTIALS) \
		semantic-release:latest \
		npx semantic-release --ci --debug

copy-makefile:
	# copies Makefile_common to all subdirs
	# This prevents a ton of copy/paste work
	for dir in $(DIRS_WITH_MAKEFILE); do \
		cp -f Makefile_common $$dir/Makefile; \
	done

setup-env: 
	PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.8 -d
	npm install
	for dir in $(DIRS_WITH_TESTS); do \
		$(MAKE) -C $$dir setup-env; \
	done

ci-setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.8 -d --ignore-pipfile
	npm ci
	for dir in $(DIRS_WITH_TESTS); do \
		$(MAKE) -C $$dir ci-setup-env; \
	done

deploy:
	pipenv run runway deploy

setup-env-target: 
	$(MAKE) -C $(TARGET) setup-env

check: 
	for dir in $(DIRS_WITH_TESTS); do \
		$(MAKE) -C $$dir check; \
	done

check-target: 
	$(MAKE) -C $(TARGET) check

.PHONY:
build:
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir build; \
	done

test:
	for dir in $(DIRS_WITH_TESTS); do \
		$(MAKE) -C $$dir test; \
	done

test-target: 
	$(MAKE) -C $(TARGET) test

test-cov:
	for dir in $(DIRS_WITH_TESTS); do \
		$(MAKE) -C $$dir test-cov; \
	done

test-cov-target: 
	$(MAKE) -C $(TARGET) test-cov

pipenv-clean: $(DIRS_WITH_MAKEFILE)
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir pipenv-clean; \
	done

pipenv-clean-target: 
	$(MAKE) -C $(TARGET) pipenv-clean

pipenv-lock: $(DIRS_WITH_MAKEFILE)
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir pipenv-lock; \
	done

pipenv-lock-target: 
	$(MAKE) -C $(TARGET) pipenv-lock

pipenv-sync: $(DIRS_WITH_MAKEFILE)
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir pipenv-sync; \
	done

pipenv-sync-target: 
	$(MAKE) -C $(TARGET) pipenv-sync

pipenv-update: $(DIRS_WITH_MAKEFILE)
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir pipenv-update; \
	done

pipenv-update-target: 
	$(MAKE) -C $(TARGET) pipenv-update


clean: $(DIRS_WITH_MAKEFILE)
	for dir in $(DIRS_WITH_MAKEFILE); do \
		$(MAKE) -C $$dir clean; \
	done

clean-target: 
	$(MAKE) -C $(TARGET) clean

install:
	@read -p "python package to install [none to install all from Pipfile]: " PACKAGE; \
	for dir in $(DIRS_WITH_TESTS) ; do \
		$(MAKE) -C $$dir install package=$$PACKAGE; \
	done 

install-dev:
	@read -p "python package to install [none to install all from Pipfile]: " PACKAGE; \
	for dir in $(DIRS_WITH_TESTS) ; do \
		$(MAKE) -C $$dir install-dev  package=$$PACKAGE; \
	done 

install-target: 
	@read -p "python package to install [none to install all from Pipfile]: " PACKAGE; \
	$(MAKE) -C $(TARGET) install package=$$PACKAGE
