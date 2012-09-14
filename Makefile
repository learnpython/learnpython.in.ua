.PHONY: bootstrap clean distclean manage server shell

ENV ?= env
PROJECT = learnpython

PYTHON = $(ENV)/bin/python
MANAGE = $(PYTHON) $(PROJECT)/manage.py

HOST ?= 0.0.0.0
PORT ?= 4351

bootstrap:
	PROJECT=$(PROJECT) bootstrap.py

clean:
	find . -name '*.pyc' -delete

distclean: clean
	rm -rf $(ENV)/
	rm $(PROJECT)/settings_local.py

manage:
	$(MANAGE) $(COMMAND)

server:
	$(MANAGE) runserver -t $(HOST) -p $(PORT)

shell:
	$(MANAGE) shell
