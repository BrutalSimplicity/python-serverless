
all: setup-env build-api-docs build-user build-admin

jenkins-build: chmod setup-python build-web

chmod:
	chmod -R ug+w .

.PHONY:
setup-env: setup-python setup-node

.PHONY: setup-python
setup-python:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d

.PHONY: 
setup-node:
	npm init -y && npm install -y

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d

build: build-api-docs build-admin build-user build-web

build-admin:
	pipenv run mkdocs --verbose build --config-file ./admin-guide/mkdocs.build.yml

build-user:
	pipenv run mkdocs --verbose build --config-file ./user-guide/mkdocs.build.yml

build-developer:
	pipenv run mkdocs --verbose build --config-file ./developer-guide/mkdocs.build.yml

build-web:
	pipenv run mkdocs --verbose build --config-file ./web/mkdocs.build.yml

.PHONY:
build-api-docs:
	./node_modules/.bin/widdershins \
		--environment api.doc.env.json \
		--user_templates ./user-guide/docs/user_templates/ \
		../runway/artifact_registry_api/artifact.registry.swagger.yml \
		--outfile ./user-guide/docs/api.md

serve:
	pipenv run mkdocs serve

serve-admin:
	pipenv run mkdocs serve -f ./admin-guide/mkdocs.build.yml

serve-user:
	pipenv run mkdocs serve -f ./user-guide/mkdocs.build.yml
