
.DEFAULT_GOAL := init

TERMINAL=get-stats-terminal.py
MAIN=$(TERMINAL)

SYS_PYTHON=$(shell which python3)
VENV_PATH=./
VENV_NAME=venv
VENV=$(VENV_PATH)$(VENV_NAME)
PIP=$(VENV)/bin/pip
PSERVE=$(VENV)/bin/pserve
PYTHON=$(VENV)/bin/python

init:
	test -e $(PYTHON) || \
		{ echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) ; } && \
	  { test -r requirements.txt && $(PIP) install -r requirements.txt ; } || \
		{ echo "No requirements.txt to install"; exit 0 ; }

test:
	$(PYTHON) -m unittest

serve: server
server:
	$(PYTHON) $(MAIN)

dev:
	$(PSERVE) development.ini --reload

run: init main
main:
	$(PYTHON) $(MAIN)

init_dev:
	test -e $(PYTHON) || \
		{ echo "Creating virtual env: $(VENV)"; $(SYS_PYTHON) -m venv $(VENV_NAME) ; } && \
		$(PIP) install --upgrade pip setuptools pipreqs && \
		$(PIP) install "pyramid==1.10.4" waitress

##
# Is this from django??
###
#install-dev:
#	$(PIP) install -e ".[dev]"

update_deps:
	$(VENV)/bin/pipreqs --force ./ 

clean:
	rm -r $(VENV) && \
	  find . -type d -name __pycache__ -exec rm -r {} \;

