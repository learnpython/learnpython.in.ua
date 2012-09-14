from flask import flash, redirect, render_template, url_for
from ordereddict import OrderedDict

from learnpython.app import pages


def index():
    courses = OrderedDict()
    names = ('medium', 'normal', 'advanced')
    page_obj = pages.get('index')

    for name in names:
        courses[name] = pages.get('courses/{0}'.format(name))

    return render_template('index.html', courses=courses, page=page_obj)


def page(name):
    page_obj = pages.get_or_404(name)
    context = {'is_{0}'.format(name): True, 'page': page_obj}
    return render_template('page.html', **context)


def subscribe():
    page_obj = pages.get('subscribe')
    return render_template('subscribe.html', page=page_obj)
