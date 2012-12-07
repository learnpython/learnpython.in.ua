from flask import url_for
from flask.ext.testing import JsonResponseMixin, TestCase as FlaskTestCase, \
    Twill as BaseTwill
from twill import commands
from webtest import TestApp

from learnpython.app import app, mail

if not hasattr(FlaskTestCase, 'assertIn'):
    from unittest2 import TestCase
    BaseTestCase = type('BaseTestCase', (FlaskTestCase, TestCase), {})
else:
    BaseTestCase = FlaskTestCase


__all__ = ('TEST_COMMENTS', 'TEST_EMAIL', 'TEST_MESSAGE', 'TEST_NAME',
           'TEST_PHONE', 'TEST_SUBJECT', 'TestCase', 'Twill')


TEST_COMMENTS = 'Test additional comments.'
TEST_EMAIL = 'iam@igordavydenko.com'
TEST_MESSAGE = 'Test message.'
TEST_NAME = 'Igor Davydenko'
TEST_PHONE = '+380 12 345-67-89'
TEST_SUBJECT = 'Test subject'


class TestCase(BaseTestCase):
    """
    Improve base test class from ``Flask-Testing`` with adding ``url`` method
    and ``udata`` property to each test client response.
    """
    ALLOW_SUBSCRIBERS = True
    BABEL_DEFAULT_LOCALE = 'en'
    CSRF_ENABLED = False
    TESTING = True

    def setUp(self):
        self.about_url = self.url('page', name='about')
        self.contacts_url = self.url('contacts')
        self.flows_url = self.url('flows')
        self.index_url = self.url('index')
        self.status_url = self.url('status')
        self.subscribe_url = self.url('subscribe')

    def tearDown(self):
        for attr in dir(self):
            if not attr.startswith('original_'):
                continue

            key = attr.replace('original_', '')
            self.app.config[key] = getattr(self, attr)

    def check_message(self, message, subject, *args):
        assert len(args) > 2
        name, email = args[:2]

        self.assertEqual(message.subject, '[Learn Python] {0}'.format(subject))
        self.assertEqual(
            message.recipients, ['we@learnpython.in.ua']
        )
        self.assertEqual(message.sender, '{0} <{1}>'.format(name, email))
        self.assertIn('Learn Python', message.body)

        for arg in args:
            self.assertIn(arg, message.body)

    def config(self, key, value):
        setattr(self, 'original_{0}'.format(key), self.app.config.get(key))
        self.app.config[key] = value

    def create_app(self):
        for attr in dir(self):
            if attr.isupper():
                app.config[attr] = getattr(self, attr)
        return app

    def url(self, *args, **kwargs):
        return url_for(*args, **kwargs)

    def _pre_setup(self):
        super(TestCase, self)._pre_setup()
        self.assertTrue(self.app.testing)

        self.app.response_class = \
            make_response_class(self._orig_response_class)
        self.client = self.app.test_client()

        mail.suppress = True
        self.mail = mail

        self.webtest = TestApp(self.app)


class Twill(BaseTwill):
    """
    Update ``Twill`` mixin class from ``Flask-Testing``. Return tuple contains
    current instance and all available twill commands on entering to context
    with ``__enter__`` method.
    """
    def __enter__(self):
        super(Twill, self).__enter__()
        return self, commands


def make_response_class(response_class):
    class TestResponse(response_class, JsonResponseMixin):
        @property
        def udata(self):
            return self.data.decode('utf-8')

    return TestResponse
