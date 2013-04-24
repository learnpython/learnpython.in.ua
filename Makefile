.PHONY: bootstrap clean compilemessages distclean killserver manage messages pep8 pylint server shell test test_selenium test_splinter test_unit test_windmill

PROJECT = learnpython

ENV ?= env
VENV = $(shell echo $(VIRTUAL_ENV))

ifneq ($(VENV),)
	BABEL = pybabel
	NOSETESTS = nosetests
	PEP8 = pep8
	PIP = pip
	PYLINT = pylint
	PYTHON = python
else
	BABEL = $(ENV)/bin/pybabel
	NOSETESTS = $(ENV)/bin/nosetests
	PEP8 = $(ENV)/bin/pep8
	PIP = $(ENV)/bin/pip
	PYLINT = $(ENV)/bin/pylint
	PYTHON = $(ENV)/bin/python
endif

COVERAGE_DIR = /tmp/$(PROJECT)-coverage
HOST ?= 0.0.0.0
PORT ?= 4351
TEST_ARGS ?= -v
TRANSLATIONS_DIR = $(PROJECT)/translations

SELENIUM_BROWSER ?= firefox
SELENIUM_HOST ?= 127.0.0.1
SELENIUM_PORT ?= 4352
SELENIUM_URL = http://$(SELENIUM_HOST):$(SELENIUM_PORT)

SPLINTER_BROWSER ?= firefox
SPLINTER_HOST ?= 127.0.0.1
SPLINTER_PORT ?= 4353
SPLINTER_URL = http://$(SPLINTER_HOST):$(SPLINTER_PORT)

WINDMILL_BROWSER ?= firefox
WINDMILL_HOST ?= 127.0.0.1
WINDMILL_PORT ?= 4354
WINDMILL_URL = http://$(WINDMILL_HOST):$(WINDMILL_PORT)

bootstrap:
	PROJECT=$(PROJECT) bootstrapper

clean:
	find . -name '*.pyc' -delete

compilemessages:
	$(BABEL) compile -f -d $(TRANSLATIONS_DIR)

deploy: test
	git push heroku master

distclean: clean
	rm -rf $(ENV)/
	rm $(PROJECT)/settings_local.py

killserver:
	kill `ps -o "pid,command" | grep "python $(PROJECT)/manage.py runserver -t $(HOST) -p $(PORT)" | grep -v grep | awk '{print $$1}'`

manage:
	$(PYTHON) $(PROJECT)/manage.py $(COMMAND)

messages:
	[ ! -d $(TRANSLATIONS_DIR) ] && mkdir $(TRANSLATIONS_DIR) || :
	$(ENV)/bin/pybabel extract -F babel.cfg -k lazy_gettext -o $(TRANSLATIONS_DIR)/messages.pot --project=$(PROJECT) .
	[ ! -d $(TRANSLATIONS_DIR)/ru ] && \
	$(BABEL) init -i $(TRANSLATIONS_DIR)/messages.pot -d $(TRANSLATIONS_DIR) -l ru || \
	$(BABEL) update -i $(TRANSLATIONS_DIR)/messages.pot -d $(TRANSLATIONS_DIR) -l ru

pep8:
	$(PEP8) --statistics $(PROJECT)/

pylint:
	$(PYLINT) $(PROJECT)/ --ignore=tests --disable=W0141,W0142

server:
	COMMAND="runserver -t $(HOST) -p $(PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test: test_selenium test_splinter test_unit

test_selenium: clean pep8
	HOST=$(SELENIUM_HOST) PORT=$(SELENIUM_PORT) $(MAKE) server &
	sleep 2

	-SELENIUM_BROWSER=$(SELENIUM_BROWSER) SELENIUM_URL=$(SELENIUM_URL) \
	$(NOSETESTS) $(TEST_ARGS) $(PROJECT)/tests/test_selenium.py

	-HOST=$(SELENIUM_HOST) PORT=$(SELENIUM_PORT) $(MAKE) killserver
	sleep 2

test_splinter: clean pep8
	HOST=$(SPLINTER_HOST) PORT=$(SPLINTER_PORT) $(MAKE) server &
	sleep 2

	-SPLINTER_BROWSER=$(SPLINTER_BROWSER) SPLINTER_URL=$(SPLINTER_URL) \
	$(NOSETESTS) $(TEST_ARGS) $(PROJECT)/tests/test_splinter.py

	-HOST=$(SPLINTER_HOST) PORT=$(SPLINTER_PORT) $(MAKE) killserver
	sleep 2

test_unit: clean pep8
	$(NOSETESTS) $(TEST_ARGS) -e "test_(selenium|splinter|windmill).py" -w $(PROJECT)/ \
	--with-coverage --cover-package=$(PROJECT) --cover-branches --cover-html --cover-html-dir=$(COVERAGE_DIR)

test_windmill: clean pep8
	HOST=$(WINDMILL_HOST) PORT=$(WINDMILL_PORT) $(MAKE) server &
	sleep 2

	-$(NOSETESTS) $(TEST_ARGS) --wmbrowser=$(WINDMILL_BROWSER) --wmtesturl=$(WINDMILL_URL) $(PROJECT)/tests/test_windmill.py

	-HOST=$(WINDMILL_HOST) PORT=$(WINDMILL_PORT) $(MAKE) killserver
	sleep 2

update:
	$(PIP) list -lo
