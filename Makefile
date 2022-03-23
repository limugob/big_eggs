PYTHON:=.venv/bin/python

.venv: $(PYTHON)

$(PYTHON):
	pyenv exec python -m venv .venv
	$(PYTHON) -m pip install -U pip wheel setuptools pip-tools

.PHONY: install
install:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: upgrade
upgrade:
	pip-compile --upgrade --output-file=requirements.txt requirements.in
