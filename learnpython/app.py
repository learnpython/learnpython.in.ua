from flask import Flask, redirect
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
views.add('/', redirect, defaults={'code': 301, 'location': '/index'})
views.add('/<any(about, index):name>', 'page')
views.add('/contacts', 'contacts', methods=('GET', 'POST'))
views.add('/flows', 'flows')
views.add('/status', 'status')
views.add('/subscribe',
          'contacts',
          defaults={'name': 'subscribe'},
          endpoint='subscribe',
          methods=('GET', 'POST'))
views.add_static('/favicon.ico', defaults={'filename': 'img/favicon.ico'})
