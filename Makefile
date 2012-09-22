.PHONY: bootstrap clean distclean manage selenium-server server shell test test_selenium test_splinter test_unit test_windmill

ENV ?= env
PROJECT = learnpython

PYTHON = $(ENV)/bin/python
MANAGE = $(PYTHON) $(PROJECT)/manage.py

HOST ?= 0.0.0.0
PORT ?= 4351
TARGET ?= octave

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
	PROJECT=$(PROJECT) bootstrap.py

clean:
	find . -name '*.pyc' -delete

deploy:
	$(ENV)/bin/fab deploy:$(TARGET)

distclean: clean
	rm -rf $(ENV)/
	rm $(PROJECT)/settings_local.py

manage:
	$(MANAGE) $(COMMAND)

selenium-server:
	java -jar $(SELENIUM_JAR)

server:
	$(MANAGE) runserver -t $(HOST) -p $(PORT)

shell:
	$(MANAGE) shell

test: test_selenium test_splinter test_unit

test_selenium: clean
	$(MAKE) selenium-server &
	sleep 10

	HOST=$(SELENIUM_HOST) PORT=$(SELENIUM_PORT) $(MAKE) server &
	sleep 2

	-SELENIUM_BROWSER=$(SELENIUM_BROWSER) SELENIUM_URL=$(SELENIUM_URL) $(ENV)/bin/nosetests $(NOSE_ARGS) -v $(PROJECT)/tests/test_selenium.py

	-kill `ps -o "pid,command" | grep "python $(PROJECT)/manage.py runserver -t $(SELENIUM_HOST) -p $(SELENIUM_PORT)" | grep -v grep | awk '{print $$1}'`
	-kill `ps -o "pid,command" | grep "java -jar $(SELENIUM_JAR)" | grep -v grep | awk '{print $$1}'`
	sleep 2

test_splinter: clean
	HOST=$(SPLINTER_HOST) PORT=$(SPLINTER_PORT) $(MAKE) server &
	sleep 2

	-SPLINTER_BROWSER=$(SPLINTER_BROWSER) SPLINTER_URL=$(SPLINTER_URL) $(ENV)/bin/nosetests $(NOSE_ARGS) -v $(PROJECT)/tests/test_splinter.py

	-kill `ps -o "pid,command" | grep "python $(PROJECT)/manage.py runserver -t $(SPLINTER_HOST) -p $(SPLINTER_PORT)" | grep -v grep | awk '{print $$1}'`
	sleep 2

test_unit: clean
	$(ENV)/bin/nosetests $(NOSE_ARGS) -e test_selenium.py -v -w $(PROJECT)/

test_windmill: clean
	HOST=$(WINDMILL_HOST) PORT=$(WINDMILL_PORT) $(MAKE) server &
	sleep 2

	-$(ENV)/bin/nosetests $(NOSE_ARGS) -v --wmbrowser=$(WINDMILL_BROWSER) --wmtesturl=$(WINDMILL_URL) $(PROJECT)/tests/test_windmill.py

	-kill `ps -o "pid,command" | grep "python $(PROJECT)/manage.py runserver -t $(WINDMILL_HOST) -p $(WINDMILL_PORT)" | grep -v grep | awk '{print $$1}'`
	sleep 2
