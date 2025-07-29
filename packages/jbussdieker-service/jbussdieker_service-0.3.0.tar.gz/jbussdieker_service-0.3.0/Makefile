.PHONY: setup test coverage format lint clean build
setup: .venv/lib/*/site-packages/__editable__.*
test: setup
	.venv/bin/python3 -m unittest tests/jbussdieker/service/test_service.py
coverage: setup .venv/bin/coverage
	.venv/bin/coverage run --source src -m unittest tests/jbussdieker/service/test_service.py
	.venv/bin/coverage report -m --fail-under=100
format: .venv/bin/black
	.venv/bin/black .
lint: .venv/bin/black .venv/bin/mypy
	.venv/bin/black --check .
	.venv/bin/mypy src/
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
.venv/bin/mypy: .venv/bin/python
	.venv/bin/pip install mypy
.venv/bin/coverage: .venv/bin/python
	.venv/bin/pip install coverage
.venv/lib/*/site-packages/__editable__.*: .venv/bin/python pyproject.toml
	.venv/bin/pip install -e .
.venv/bin/python:
	python3 -m venv .venv
