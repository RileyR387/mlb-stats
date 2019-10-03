
.DEFAULT_GOAL := init

MAIN=get-stats-terminal.py

SYS_PYTHON=$(shell which python3)
VENV_PATH=./
VENV_NAME=venv
VENV=$(VENV_PATH)$(VENV_NAME)
PIP=$(VENV)/bin/pip
PYTHON=$(VENV)/bin/python

init:
	test -e $(PYTHON) || { $(SYS_PYTHON) -m venv $(VENV_NAME) && $(PIP) install --upgrade pip setuptools wheel ; }

test: init
	$(PYTHON) -m unittest

install:
	$(PIP) install .

install-dev: init
	test -e $(PYTHON) || \
    $(PIP) install -e ".[dev]"

install-user: test
	$(PIP) install --user .

install-site:
	$(SYS_PYTHON) -m pip install .

run: init
	$(PYTHON) $(MAIN)

pin-dependencies:
	$(PIP) install --upgrade pipreqs && \
  $(VENV)/bin/pipreqs --force ./

clean:
	find . -type d -name "*egg-info" -exec rm -r {} \; 2>/dev/null ; \
  find . -type d -name __pycache__ -not -path $(VENV) -exec rm -r {} \; 2>/dev/null && \
    echo "So fresh so clean..."

clean-venv:
	test -d ./venv &&  \
    rm -r ./venv || echo "./venv already clean!"

clean-all: clean clean-venv

