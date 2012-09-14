from flask import Flask
from flask.ext.babel import Babel
from flask.ext.flatpages import FlatPages
from flask.ext.lazyviews import LazyViews
from flask.ext.script import Manager

from learnpython import settings


app = Flask('learnpython')
app.config.from_object(settings)

babel = Babel(app)

manager = Manager(app)

pages = FlatPages(app)

views = LazyViews(app, 'learnpython.views')
views.add('/', 'index')
views.add('/<any(about, contacts):name>', 'page')
views.add('/subscribe', 'subscribe')
