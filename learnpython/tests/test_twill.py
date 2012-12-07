import sys

from random import choice, randint

from twill.commands import config

from learnpython.app import pages

from .common import TEST_COMMENTS, TEST_EMAIL, TEST_MESSAGE, TEST_NAME, \
    TEST_PHONE, TEST_SUBJECT, TestCase, Twill


IS_PYTHON_26 = sys.version_info[:2] == (2, 6)


class TestViewsWithTwill(TestCase):

    def tearDown(self):
        self.enable_redirect()

    def check_page(self, name, url):
        page = pages.get(name)
        self.assertIsNotNone(page)

        with Twill(self.app, port=self.port) as (t, c):
            url = t.url(url)
            c.go(url)
            c.url(url + '$')
            c.code(200)
            c.find(u'<h2>{0}</h2>'.format(page['title']).encode('utf-8'))

    def disable_redirect(self, c=None):
        func = c.config if c else config
        self.old_redirect = func('acknowledge_equiv_refresh')
        func('acknowledge_equiv_refresh', False)

    def enable_redirect(self, c=None):
        if hasattr(self, 'old_redirect'):
            delattr(self, 'old_redirect')

        func = c.config if c else config
        func('acknowledge_equiv_refresh', True)

    @property
    def port(self):
        return randint(10000, 20000)

    def test_about(self):
        self.check_page('about', self.about_url)

    def test_contacts(self):
        self.check_page('contacts', self.contacts_url)

        with Twill(self.app, port=self.port) as (t, c):
            self.disable_redirect(c)

            c.go(t.url(self.contacts_url))
            c.code(200)

            c.submit()
            c.code(200)
            c.url(t.url(self.contacts_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', '')
            c.fv(1, 'email', TEST_EMAIL)
            c.fv(1, 'message', TEST_MESSAGE)

            c.submit()
            c.code(200)
            c.url(t.url(self.contacts_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', '')
            c.fv(1, 'message', TEST_MESSAGE)

            c.submit()
            c.code(200)
            c.url(t.url(self.contacts_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_EMAIL)
            c.fv(1, 'message', '')

            c.submit()
            c.code(200)
            c.url(t.url(self.contacts_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_NAME)
            c.fv(1, 'message', TEST_MESSAGE)

            c.submit()
            c.code(200)
            c.url(t.url(self.contacts_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('Invalid email address.')
            c.notfind('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_EMAIL)
            c.fv(1, 'message', TEST_MESSAGE)

            with self.mail.record_messages() as outbox:
                c.submit()
                c.code(200)
                c.url(t.url(self.status_url))

                self.assertEqual(len(outbox), 1)
                args = (TEST_NAME, TEST_EMAIL, TEST_MESSAGE)
                self.check_message(outbox[0], 'Feedback', *args)

            c.go(t.url(self.contacts_url))
            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_EMAIL)
            c.fv(1, 'subject', TEST_SUBJECT)
            c.fv(1, 'message', TEST_MESSAGE)

            with self.mail.record_messages() as outbox:
                c.submit()
                c.code(200)
                c.url(t.url(self.status_url))

                self.assertEqual(len(outbox), 1)
                self.check_message(outbox[0], TEST_SUBJECT, *args)

    def test_flows(self):
        flows = filter(lambda item: item[0].startswith('flows/'),
                       pages._pages.items())

        with Twill(self.app, port=self.port) as (t, c):
            c.go(t.url(self.flows_url))
            c.code(200)

            for fullname, flow in flows:
                name = fullname.replace('flows/', '')
                c.find('id="{0}"'.format(name))

    def test_index(self):
        with Twill(self.app, port=self.port) as (t, c):
            c.go(t.url('/'))
            c.url(t.url(self.index_url) + '$')

            self.check_page('index', self.index_url)

            c.go(t.url(self.index_url))

            c.follow('About us')
            c.code(200)
            c.url(t.url(self.about_url))

            c.follow('Contacts')
            c.code(200)
            c.url(t.url(self.contacts_url))

            c.follow('Subscribe')
            c.code(200)
            c.url(t.url(self.subscribe_url))

            if IS_PYTHON_26:
                c.go(t.url(self.flows_url))
                c.code(200)
                c.find('Web flow')
                c.find('Advanced flow')

                c.find('<div class="active tab" id="web">')
                c.find('<div class="tab" id="advanced">')
            else:
                c.follow('Web flow')
                c.code(200)
                c.url(t.url(self.flows_url) + '#web$')

                c.follow('Advanced flow')
                c.code(200)
                c.url(t.url(self.flows_url) + '#advanced$')

            c.follow('Learn Python')
            c.code(200)
            c.url(t.url(self.index_url))

    def test_nosubscribe(self):
        self.config('ALLOW_SUBSCRIBERS', False)

        with Twill(self.app, port=self.port) as (t, c):
            c.go(t.url(self.subscribe_url))
            c.code(200)
            c.notfind('<form action="" ')
            c.find('<h2>')

    def test_static(self):
        url200 = self.url('static', filename='css/screen.css')
        url404 = self.url('static', filename='does_not_exists.exe')

        with Twill(self.app, port=self.port) as (t, c):
            c.go(t.url(url200))
            c.code(200)

            c.go(t.url(url404))
            c.code(404)

    def test_subscribe(self):
        self.check_page('subscribe', self.subscribe_url)

        with Twill(self.app, port=self.port) as (t, c):
            self.disable_redirect(c)

            c.go(t.url(self.subscribe_url))
            c.code(200)

            c.submit()
            c.code(200)
            c.url(t.url(self.subscribe_url) + '$')

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', '')

            c.submit()
            c.code(200)

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', '')
            c.fv(1, 'email', TEST_EMAIL)

            c.submit()
            c.code(200)

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_NAME)

            c.submit()
            c.code(200)

            c.find('Cannot submit form! Please, fix errors below:')
            c.find('Invalid email address.')
            c.notfind('This field is required.')

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_EMAIL)

            with self.mail.record_messages() as outbox:
                c.submit()
                c.code(200)
                c.url(t.url(self.status_url))

                self.assertEqual(len(outbox), 1)
                args = (TEST_NAME, TEST_EMAIL, 'web')
                self.check_message(outbox[0], 'Subscribe', *args)

            c.go(self.subscribe_url)
            flow = choice(('web', 'advanced'))

            c.fv(1, 'name', TEST_NAME)
            c.fv(1, 'email', TEST_EMAIL)
            c.fv(1, 'phone', TEST_PHONE)
            c.fv(1, 'flow', flow)
            c.fv(1, 'comments', TEST_COMMENTS)

            with self.mail.record_messages() as outbox:
                c.submit()
                c.code(200)
                c.url(t.url(self.status_url))

                self.assertEqual(len(outbox), 1)
                args = (TEST_NAME, TEST_EMAIL, TEST_PHONE, flow, TEST_COMMENTS)
                self.check_message(outbox[0], 'Subscribe', *args)
