import socket

from flask import flash, render_template, redirect, request, url_for
from flask.ext.babel import lazy_gettext as _
from ordereddict import OrderedDict

from learnpython.app import pages
from learnpython.forms import ContactsForm, SubscribeForm


def contacts(name=None):
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

    form_klass = globals()[name.title() + 'Form']
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


def flows():
    data = filter(lambda item: item[0].startswith('flows/'),
                  pages._pages.items())
    data = map(lambda item: (item[0].replace('flows/', ''), item[1]), data)
    data.sort(key=lambda item: item[1]['order'])
    return render_template('flows.html', flows=OrderedDict(data))


def page(name):
    page_obj = pages.get_or_404(name)
    context = {'is_{0}'.format(name): True, 'page': page_obj}
    return render_template('page.html', **context)


def status():
    next = request.args.get('next', request.referrer or url_for('index'))
    return render_template('status.html', next=next)
