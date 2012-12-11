"""
====================
learnpython.settings
====================

Default configuration for Learn Python site.

You could customize things by overwrite these or other settings of Flask and
other used extensions in ``settings_local`` module which should placed next to
current one.

"""

import os


DIRNAME = os.path.abspath(os.path.dirname(__file__))
env = os.environ.get
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

# Debug settings
DEBUG = False

# Babel settings
BABEL_DEFAULT_LOCALE = 'ru'
BABEL_DEFAULT_TIMEZONE = 'Europe/Kiev'

# FlatPages settings
FLATPAGES_EXTENSION = '.yml'
FLATPAGES_HTML_RENDERER = 'learnpython.utils:restructuredtext_filter'
FLATPAGES_ROOT = rel('data')

# Mail settings
DEFAULT_MAIL_SENDER = 'Learn Python <we@learnpython.in.ua>'
MAIL_FAIL_SILENTLY = False
MAIL_SERVER = env('MAILGUN_SMTP_SERVER', 'localhost')
MAIL_PORT = env('MAILGUN_SMTP_PORT', 25)
MAIL_USERNAME = env('MAILGUN_SMTP_LOGIN', '')
MAIL_PASSWORD = env('MAILGUN_SMTP_PASSWORD', '')

# WTForms settings
SECRET_KEY = env('SECRET_KEY', 'Z\xc7G\xaf\x15$\xc1O\x8d\xb0Bks\x9b\n\x9a')

# Project-related settings
ALLOW_SUBSCRIBERS = bool(int(env('ALLOW_SUBSCRIBERS', 1)))
MAIL_RECIPIENTS = env('MAIL_RECIPIENTS', 'we@learnpython.in.ua').split(',')


# Import local settings if any
try:
    from learnpython import settings_local
except ImportError:
    pass
else:
    for attr in dir(settings_local):
        if attr.startswith('_'):
            continue
        locals()[attr] = getattr(settings_local, attr)
