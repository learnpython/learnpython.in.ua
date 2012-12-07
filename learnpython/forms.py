"""
=================
learnpython.forms
=================

Contacts and subscribe form for Learn Python site.

All forms are built on top of ``Flask-WTF`` extension, all emails will send
using ``Flask-Mail`` extension.

Default recipient
=================

By default, all emails will sent to ``BaseContactsForm.default_recipient``
email. To customize things, setup ``MAIL_RECIPIENTS`` setting with tuple or
list of recipients.

"""

from flask import render_template
from flask.ext import wtf
from flask.ext.babel import lazy_gettext as _
from flask.ext.mail import Message

from learnpython.app import app, mail, pages


__all__ = ('ContactsForm', 'SubscribeForm')


FLOW_CHOICES = \
    map(lambda item: (item[0].replace('flows/', ''), item[1]['title']),
        sorted(filter(lambda item: item[0].startswith('flows/'),
                      pages._pages.items()),
               key=lambda item: item[1]['order']))


class Email(wtf.Email, object):
    """
    Localize message for email validator.
    """
    def __init__(self, message=None):
        message = message or _('Invalid email address.')
        super(Email, self).__init__(message)


class Required(wtf.Required, object):
    """
    Localize message for required validator.
    """
    def __init__(self, message=None):
        message = message or _('This field is required.')
        super(Required, self).__init__(message)


class BaseContactsForm(wtf.Form, object):
    """
    Base contacts form.

    Provide common fields, config settings and method to send email after
    succeed form validation.
    """
    name = wtf.TextField(_('Name'), validators=[Required()])
    email = wtf.TextField(_('Email'), validators=[Required(), Email()])

    default_recipient = 'we@learnpython.in.ua'
    template = None
    title = None

    @property
    def recipients(self):
        """
        Read list of recipients from application config.
        """
        default = [self.default_recipient]
        return app.config.get('MAIL_RECIPIENTS', default)

    def send(self):
        """
        Send email to all form recipients.
        """
        assert self.title, 'Please, supply "title" attribute first.'
        assert self.template, 'Please, supply "template" attribute first.'

        message = Message(u'[Learn Python] {0}'.format(self.title),
                          sender=(self.data['name'], self.data['email']),
                          recipients=self.recipients)
        message.body = render_template(self.template, **self.data)

        mail.send(message)


class ContactsForm(BaseContactsForm):
    """
    Feedback form.
    """
    subject = wtf.TextField(_('Subject'))
    message = wtf.TextField(
        _('Message'), validators=[Required()], widget=wtf.TextArea()
    )

    template = 'mails/contacts.txt'
    title = _('Feedback')

    def send(self):
        """
        Use custom subject for email message if user filled in "Subject" field.
        """
        self.title = self.data['subject'] or self.title
        super(ContactsForm, self).send()


class SubscribeForm(BaseContactsForm):
    """
    Subscribe form.
    """
    phone = wtf.TextField(_('Phone'))
    flow = wtf.SelectField(
        _('Flow'), choices=FLOW_CHOICES, validators=[Required()]
    )
    comments = wtf.TextField(_('Additional comments'), widget=wtf.TextArea())

    template = 'mails/subscribe.txt'
    title = _('Subscribe')
