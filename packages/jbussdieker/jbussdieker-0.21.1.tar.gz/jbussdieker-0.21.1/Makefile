.PHONY: all install test-installed upgrade setup test coverage format lint clean build

all: coverage
install:
	pip install --break-system .
test-installed:
	python3 -m unittest discover
upgrade:
	pip install --upgrade --break-system jbussdieker
setup: .venv/lib/*/site-packages/__editable__.*
test: setup
	.venv/bin/python3 -m unittest tests/test_*.py
coverage: setup .venv/bin/coverage
	.venv/bin/coverage run --source src -m unittest tests/test_*.py
	.venv/bin/coverage report -m --fail-under=100
format: .venv/bin/black
	.venv/bin/black .
lint: .venv/bin/black
	.venv/bin/black --check .
build: .venv/bin/build
	.venv/bin/python -m build .
build-check: .venv/bin/twine
	.venv/bin/twine check dist/*
publish-test: .venv/bin/twine
	.venv/bin/twine upload --repository testpypi dist/*
publish: .venv/bin/twine
	.venv/bin/twine upload dist/*
.venv/bin/build: .venv/bin/python
	.venv/bin/pip install build
clean:
	rm -rf dist build .venv
.venv/bin/twine: .venv/bin/python
	.venv/bin/pip install twine
.venv/bin/black: .venv/bin/python
	.venv/bin/pip install black
.venv/bin/coverage: .venv/bin/python
	.venv/bin/pip install coverage
.venv/lib/*/site-packages/__editable__.*: .venv/bin/python pyproject.toml
	.venv/bin/pip install -e .
.venv/bin/python:
	python3 -m venv .venv
