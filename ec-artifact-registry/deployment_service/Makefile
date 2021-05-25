# This file is copied from Makefile_common, and is overwritten with `make copy-makefile` in the root dir
# to make changes, make them in the Makefile_common in the root dir, and run `make copy-makefile`

ifeq ($(shell test -f .env),yes)
include .env
export $(shell sed 's/=.*//' .env)
endif

CLEAN_FILE_TARGETS = package .coverage dir_hash_zip *.zip requirements.txt
CLEAN_DIR_TARGETS = venv .venv .pytest_cache _build _dist __pycache__

current_dir := $(shell pwd)
source_directory = $(current_dir)/src
tests_directoy = $(current_dir)/tests
build_directory = $(current_dir)/_build
dist_directory = $(current_dir)/_dist
dist_filename = lambda.zip

all: clean setup-env test check build

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.8 -d
	npm install

.PHONY:
check:
	pipenv run safety check

sync:
	pipenv sync

test:
	pipenv run pytest -s --cache-clear $(tests_directoy)

test-cov:
	pipenv run pytest --cov=src --cov-report=term --cov-report=xml:cov.xml $(tests_directoy)

.PHONY:
$(build_directory):
	@echo \>\>\> creating $(build_directory)
	@mkdir -p $(build_directory)

.PHONY:
$(dist_directory):
	@echo \>\>\> creating $(dist_directory)
	@mkdir -p $(dist_directory)

.ONESHELL:
.PHONY: 
build-install: 
	@echo \>\>\> installing pipenv dependencies to $(build_directory)
	$(shell pipenv lock -r > requirements.txt)
	pipenv --verbose run pip install -r requirements.txt --target $(build_directory)

.PHONY:
build-copy-source:
	@echo \>\>\> copying source to $(build_directory)
	@cp -RL $(source_directory)/* $(build_directory) 

.PHONY:
build-package:
	@echo \>\>\> packaging $(build_directory)
	cd $(build_directory); \
	zip -r9q $(dist_directory)/$(dist_filename) .; 

.PHONY:
build: | $(build_directory) $(dist_directory) build-install build-copy-source build-package

pipenv-clean:
	pipenv clean

pipenv-lock:
	pipenv lock

pipenv-sync:
	pipenv sync

pipenv-update:
	pipenv update

clean-files:
	for target in $(CLEAN_FILE_TARGETS); do \
		find . -name $$target -delete; \
	done

clean-dirs:
	for target in $(CLEAN_DIR_TARGETS); do \
		rm -rf $$target ; \
	done

clean: clean-dirs clean-files

install:
	@echo installing package: $(package)
	pipenv install $(package)

install-dev:
	@echo installing package: $(package)
	pipenv install $(package) --dev
