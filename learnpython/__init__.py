"""
===========
learnpython
===========

Web-site for `Learn Python <http://learnpython.in.ua/>`_ courses built on top
of `Flask <http://flask.pocoo.org/>`_ micro-framework.

Python parts
============

As site built on top of Flask it main element is ``app`` module, where all
necessary definitions and configuration happened.

Settings are stored in ``settings`` module and could be rewrite with local ones
from ``settings_local`` module.

Views and all code required for views stored in ``views``, ``forms`` and
``utils`` modules. But view registration done in ``app`` using lazy-add
technique.

And finally, several different tests are stored in ``tests`` package.

Data parts
==========

For data storage site using plain files, which placed in ``data/`` directory,
later these files processed using ``Flask-FlatPages`` extension.

"""
