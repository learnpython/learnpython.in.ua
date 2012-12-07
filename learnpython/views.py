"""
=================
learnpython.views
=================

View functions for Learn Python web-site.

"""

import socket

from flask import flash, render_template, redirect, request, url_for
from flask.ext.babel import lazy_gettext as _
from ordereddict import OrderedDict

from learnpython import forms
from learnpython.app import pages


def contacts(name=None):
    """
    Contacts form or subscribe page.

    Add ability to send email with question about cources or subscribe to
    lessons.
    """
    messages = {
        'contacts': {
            'error': _('Cannot send message due to mail server problems. '
                       'Please, try again later!'),
            'success': _('Your message has been sent! Thanks for your '
                         'feedback!'),
        },
        'subscribe': {
            'error': _('Cannot apply subscription due to mail server '
                       'problems. Please, try again later!'),
            'success': _('You successfully subscribed to Learn Python '
                         'courses! We will send you all necessary information '
                         'later!')
        }
    }
    name = name or 'contacts'

    form_klass = getattr(forms, name.title() + 'Form')
    page_obj = pages.get(name)

    if request.method == 'POST':
        form = form_klass(request.form)

        if form.validate():
            try:
                form.send()
            except socket.error:
                flash(messages[name]['error'], 'error')
            else:
                flash(messages[name]['success'])

            return redirect(url_for('status', next=request.path))
    else:
        form = form_klass()

    context = {'form': form, 'is_{0}'.format(name): True, 'page': page_obj}
    return render_template('contacts.html', **context)


def error(err):
    """
    Error page.

    Prettify "Does Not Exist" and "Server Error" errors handling by displaying
    fancy page.
    """
    code = getattr(err, 'code', 500)
    return render_template('error.html', error=err), code


def flows():
    """
    Flows page.

    Show information of all available flows, which available in courses.
    """
    data = filter(lambda item: item[0].startswith('flows/'),
                  pages._pages.items())
    data = map(lambda item: (item[0].replace('flows/', ''), item[1]), data)
    data.sort(key=lambda item: item[1]['order'])
    return render_template('flows.html', flows=OrderedDict(data))


def page(name):
    """
    Flat page.

    Show content of flat page, which named ``name``. Content of flat page would
    be rendered with ReStructuredText markup.

    If page not found - show "Does Not Exist" error page.
    """
    page_obj = pages.get_or_404(name)
    context = {'is_{0}'.format(name): True, 'page': page_obj}
    return render_template('page.html', **context)


def status():
    """
    Status page.

    Helper page, which displays after user sent message or has been subscribed.
    """
    next_page = request.args.get('next', request.referrer or url_for('index'))
    return render_template('status.html', next=next_page)
