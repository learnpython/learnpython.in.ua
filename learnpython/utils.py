"""
=================
learnpython.utils
=================

Utilities and helpers for Learn Python site.

"""

from docutils.core import publish_parts
from flask import current_app
from jinja2.filters import do_mark_safe


__all__ = ('restructuredtext_filter', )


def restructuredtext_filter(text, result=None):
    """
    Convert text to HTML using reStructuredText markup.
    """
    app = current_app

    docutils_settings = app.config.get('RESTRUCTUREDTEXT_FILTER_SETTINGS', {})
    result = result or 'fragment'
    writer_name = app.config.get('RESTRUCTUREDTEXT_WRITER_NAME', 'html4css1')

    parts = publish_parts(source=text,
                          writer_name=writer_name,
                          settings_overrides=docutils_settings)
    return do_mark_safe(parts[result])
