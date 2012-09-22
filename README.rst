=================
learnpython.in.ua
=================

Learn Python web-site.

Requirements
============

* `Python <http://www.python.org/>`_ 2.6 or 2.7
* `Make <http://www.gnu.org/make>`_
* `virtualenv <http://www.virtualenv.org/>`_ 1.6 or higher

Installation
============

You just need to bootstrap project, with::

    $ make bootstrap

After, all necessary would be created and project will be ready to deploy.

Usage
=====

First, you need to run development web-server or host WSGI application somehow
you usually do (maybe with uwsgi or gunicorn). For dev server, execute::

    $ make server

By default, this runs server at ``4351`` port. So, point your browser to
``http://127.0.0.1:4351/`` to see results.

For uwsgi or gunicorn config use::

    learnpython.app:app

application notation.

Testing
=======

To run all tests, execute::

    $ make test

But, you should customize running tests by specifying one of next targets,

:test_selenium: Prepare and run selenium tests
:test_unit: Run only unit tests
