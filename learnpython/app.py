"""
===============
learnpython.app
===============

Flask application for Learn Python web-site.

Used extensions
===============

* `Flask-Babel <http://packages.python.org/Flask-Babel/>`_
* `Flask-FlatPages <http://packages.python.org/Flask-FlatPages/>`_
* `Flask-LazyViews <http://pypi.python.org/pypi/Flask-LazyViews>`_
* `Flask-Mail <http://packages.python.org/Flask-Mail/>`_
* `Flask-Script <http://flask-script.readthedocs.org/en/latest/>`_
* `Flask-Testing <http://packages.python.org/Flask-Testing/>`_
* `Flask-WTF <http://packages.python.org/Flask-WTF/>`_

"""

from flask import Flask
from flask.ext.babel import Babel
from flask.ext.flatpages import FlatPages
from flask.ext.lazyviews import LazyViews
from flask.ext.mail import Mail
from flask.ext.script import Manager

from learnpython import settings


# Initialize Flask application
app = Flask('learnpython')
app.config.from_object(settings)

# Configure all necessary plugins
babel = Babel(app)
mail = Mail(app)
manager = Manager(app)
pages = FlatPages(app)

# Register all possible urls
views = LazyViews(app, '.views')
views.add('/', 'page', defaults={'name': 'index'}, endpoint='index')
views.add('/contacts', 'contacts', methods=('GET', 'POST'))
views.add('/flows', 'flows')
views.add('/status', 'status')
views.add('/subscribe', 'subscribe', methods=('GET', 'POST'))
views.add_error(404, 'error')
views.add_error(500, 'error')
views.add_static('/favicon.ico', defaults={'filename': 'img/favicon.ico'})
views.add('/<path:name>', 'page')
