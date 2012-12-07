#!/usr/bin/env python
"""
==================
learnpython.manage
==================

Run management commands using ``Flask-Script`` extension.

To get all available commands run this file without arguments, like::

    $ ./manage.py

"""

from learnpython.app import manager


if __name__ == '__main__':
    manager.run()
