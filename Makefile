.PHONY: venv install-dev test coverage lint format typecheck package deploy

venv:
	python -m venv venv

install-dev: venv
	venv/bin/pip install -r requirements-dev.txt
	venv/bin/pre-commit install

test: install-dev
	venv/bin/pytest test/

coverage: install-dev
	venv/bin/pytest --cov=src --cov-report=term-missing --cov-report=xml test/

lint: install-dev
	venv/bin/ruff check src test

fix: install-dev
	venv/bin/ruff check src test --fix

format: install-dev
	venv/bin/ruff format .

typecheck: install-dev
	venv/bin/pyrefly check src test

all: lint format typecheck coverage

package:
	rm -rf package lambda_deployment_package.zip
	mkdir package
	pip install -r requirements.txt -t package/
	cp -r src/khc package/
	cp src/khc/app.py package/
	cd package && zip -r ../lambda_deployment_package.zip .

deploy: package
	aws lambda update-function-code --function-name KurzeHosenChecker --zip-file fileb://lambda_deployment_package.zip
