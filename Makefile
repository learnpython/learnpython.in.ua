.PHONY: bootstrap clean compilemessages distclean killselenium killserver manage messages pep8 pylint selenium server shell test test_selenium test_splinter test_unit test_windmill

ENV ?= env
PROJECT = learnpython
TRANSLATIONS_DIR = $(PROJECT)/translations

PYTHON = $(ENV)/bin/python
MANAGE = $(PYTHON) $(PROJECT)/manage.py

HOST ?= 0.0.0.0
PORT ?= 4351

SELENIUM_BROWSER ?= firefox
SELENIUM_JAR ?= $(ENV)/bin/selenium-server-standalone-2.25.0.jar
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
	$(ENV)/bin/pybabel compile -f -d $(TRANSLATIONS_DIR)

deploy: pep8 test
	git push heroku master

distclean: clean
	rm -rf $(ENV)/
	rm $(PROJECT)/settings_local.py

killselenium:
	kill `ps -o "pid,command" | grep "java -jar $(SELENIUM_JAR)" | grep -v grep | awk '{print $$1}'`

killserver:
	kill `ps -o "pid,command" | grep "python $(PROJECT)/manage.py runserver -t $(HOST) -p $(PORT)" | grep -v grep | awk '{print $$1}'`

manage:
	$(MANAGE) $(COMMAND)

messages:
	[ ! -d $(TRANSLATIONS_DIR) ] && mkdir $(TRANSLATIONS_DIR) || :
	$(ENV)/bin/pybabel extract -F babel.cfg -k lazy_gettext -o $(TRANSLATIONS_DIR)/messages.pot --project=$(PROJECT) .
	[ ! -d $(TRANSLATIONS_DIR)/ru ] && \
	$(ENV)/bin/pybabel init -i $(TRANSLATIONS_DIR)/messages.pot -d $(TRANSLATIONS_DIR) -l ru || \
	$(ENV)/bin/pybabel update -i $(TRANSLATIONS_DIR)/messages.pot -d $(TRANSLATIONS_DIR) -l ru

pep8:
	$(ENV)/bin/pep8 --count --statistics $(PROJECT)/

pylint:
	$(ENV)/bin/pylint $(PROJECT)/ --ignore=tests --disable=W0141,W0142

selenium:
	java -jar $(SELENIUM_JAR)

server:
	$(MANAGE) runserver -t $(HOST) -p $(PORT)

shell:
	$(MANAGE) shell

test: test_selenium test_splinter test_unit

test_selenium: clean
	HOST=$(SELENIUM_HOST) PORT=$(SELENIUM_PORT) $(MAKE) server &
	sleep 2

	-SELENIUM_BROWSER=$(SELENIUM_BROWSER) SELENIUM_URL=$(SELENIUM_URL) $(ENV)/bin/nosetests $(NOSE_ARGS) -v $(PROJECT)/tests/test_selenium.py

	-HOST=$(SELENIUM_HOST) PORT=$(SELENIUM_PORT) $(MAKE) killserver
	sleep 2

test_splinter: clean
	HOST=$(SPLINTER_HOST) PORT=$(SPLINTER_PORT) $(MAKE) server &
	sleep 2

	-SPLINTER_BROWSER=$(SPLINTER_BROWSER) SPLINTER_URL=$(SPLINTER_URL) $(ENV)/bin/nosetests $(NOSE_ARGS) -v $(PROJECT)/tests/test_splinter.py

	-HOST=$(SPLINTER_HOST) PORT=$(SPLINTER_PORT) $(MAKE) killserver
	sleep 2

test_unit: clean
	$(ENV)/bin/nosetests $(NOSE_ARGS) -e "test_(selenium|splinter|windmill).py" -v -w $(PROJECT)/

test_windmill: clean
	HOST=$(WINDMILL_HOST) PORT=$(WINDMILL_PORT) $(MAKE) server &
	sleep 2

	-$(ENV)/bin/nosetests $(NOSE_ARGS) -v --wmbrowser=$(WINDMILL_BROWSER) --wmtesturl=$(WINDMILL_URL) $(PROJECT)/tests/test_windmill.py

	-HOST=$(WINDMILL_HOST) PORT=$(WINDMILL_PORT) $(MAKE) killserver
	sleep 2
