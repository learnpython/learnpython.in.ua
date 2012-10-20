from flask import render_template
from flask.ext import wtf
from flask.ext.babel import lazy_gettext as _
from flask.ext.mail import Message

from learnpython.app import mail, pages


__all__ = ('ContactsForm', 'SubscribeForm')


FLOW_CHOICES = \
    map(lambda item: (item[0].replace('flows/', ''), item[1]['title']),
        sorted(filter(lambda item: item[0].startswith('flows/'),
                      pages._pages.items()),
               key=lambda item: item[1]['order']))


class Email(wtf.Email):
    """
    Localize message for email validator.
    """
    def __init__(self, message=None):
        message = message or _('Invalid email address.')
        super(Email, self).__init__(message)


class Required(wtf.Required):
    """
    Localize message for required validator.
    """
    def __init__(self, message=None):
        message = message or _('This field is required.')
        super(Required, self).__init__(message)


class BaseContactsForm(wtf.Form):
    """
    Base contacts form.

    Provide common fields, config settings and method to send email after
    succeed form validation.
    """
    name = wtf.TextField(_('Name'), validators=[Required()])
    email = wtf.TextField(_('Email'), validators=[Required(), Email()])

    recipients = ['we@learnpython.in.ua']
    template = None
    title = None

    def send(self):
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
    message = wtf.TextField(_('Message'), validators=[Required()],
        widget=wtf.TextArea())

    template = 'mails/contacts.txt'
    title = _('Feedback')

    def send(self):
        self.title = self.data['subject'] or self.title
        super(ContactsForm, self).send()


class SubscribeForm(BaseContactsForm):
    """
    Subscribe form.
    """
    phone = wtf.TextField(_('Phone'))
    flow = wtf.SelectField(_('Flow'), choices=FLOW_CHOICES,
        validators=[Required()])
    comments = wtf.TextField(_('Additional comments'), widget=wtf.TextArea())

    template = 'mails/subscribe.txt'
    title = _('Subscribe')
