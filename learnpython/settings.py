import os


DIRNAME = os.path.abspath(os.path.dirname(__file__))
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


# Import local settings if any
try:
    import settings_local
except ImportError:
    pass
else:
    for attr in dir(settings_local):
        if attr.startswith('_'):
            continue
        locals()[attr] = getattr(settings_local, attr)
