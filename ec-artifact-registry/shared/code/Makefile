# This file is copied from Makefile_common, and is overwritten with `make copy-makefile` in the root dir
# to make changes, make them in the Makefile_common in the root dir, and run `make copy-makefile`

# source any config via .env file
${shell . .env}

current_dir := $(shell pwd)

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.8 -d

check:
	pipenv check

sync:
	pipenv sync

test:
	pipenv run pytest -rfEp --full-trace -s -vvv $(current_dir)/tests/

test-cov:
	pipenv run pytest --cov=src --cov-report=term --cov-report=xml:cov.xml $(current_dir)/tests/

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
	@echo 'clean'
	rm -rf package
	rm -rf .coverage
	rm -rf dist
	rm -rf venv
	rm -rf .venv
	rm -rf .pytest_cache
	rm -f dir_hash_zip
	rm *.zip

install:
	@echo installing package: $(package)
	pipenv install $(package)
