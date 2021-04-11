setup-env:
	poetry install -v
	npm install

code-check:
	poetry run flake8 -v

test: code-check
	poetry run pytest tests -s -vvv tests/

test-cov:
	poetry run pytest tests --cov=cumulus --cov-report=term --cov-report=xml:cov.xml tests/

# ***************
# CI Commands
# ***************

ci-setup-env:
	pyenv local 3.8.0 3.9.0
	poetry install --no-dev
	npm ci

	
ci-code-check:
	flake8 -v
	npx pyright

ci-test:
	tox --recreate
