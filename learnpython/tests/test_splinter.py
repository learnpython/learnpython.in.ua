import os

from unittest import TestCase

from flask import url_for
from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError
from werkzeug.routing import BuildError

from learnpython.app import app


class TestViewsWithSplinter(TestCase):

    def setUp(self):
        app.testing = True
        self._ctx = app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

        if hasattr(self, '_browser_cache'):
            self.browser.quit()

    @property
    def browser(self):
        if not hasattr(self, '_browser_cache'):
            browser_name = os.environ.get('SPLINTER_BROWSER', 'firefox')
            browser = Browser(browser_name)
            setattr(self, '_browser_cache', browser)
        return getattr(self, '_browser_cache')

    @property
    def host(self):
        default = 'http://127.0.0.1:5001'
        return os.environ.get('SPLINTER_URL', default)

    def url(self, url_rule, *args, **kwargs):
        try:
            url = url_for(url_rule, *args, **kwargs)
        except BuildError:
            url = url_rule
        return self.host + url

    def test_index(self):
        index_url = self.url('index')

        self.browser.visit(index_url)
        self.assertEqual(self.browser.url, index_url)

        link = self.browser.find_link_by_text('Learn Python')
        self.assertEqual(len(link), 1)
        self.assertEqual(link[0].text, 'Learn Python')

    def test_static(self):
        self.browser.visit(self.url('static', filename='css/screen.css'))
        self.assertEqual(self.browser.status_code.code, 200)

        self.assertRaises(
            HttpResponseError,
            self.browser.visit,
            self.url('static', filename='does_not_exist.exe')
        )
