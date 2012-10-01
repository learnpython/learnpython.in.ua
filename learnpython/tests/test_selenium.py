import os
import time

from unittest import TestCase

from flask import url_for
from selenium import webdriver
from werkzeug.routing import BuildError

from learnpython.app import app


SELENIUM_BROWSERS = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'ie': webdriver.Ie,
    'opera': webdriver.Opera,
}


class TestViewsWithSelenium(TestCase):

    def setUp(self):
        app.testing = True
        self._ctx = app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()
        self.browser.quit()

    @property
    def browser(self):
        if not hasattr(self, '_browser_cache'):
            browser_name = os.environ.get('SELENIUM_BROWSER', 'firefox')
            self.assertIn(browser_name, SELENIUM_BROWSERS)
            browser = SELENIUM_BROWSERS[browser_name]()
            setattr(self, '_browser_cache', browser)
        return getattr(self, '_browser_cache')

    @property
    def host(self):
        default = 'http://127.0.0.1:5001'
        return os.environ.get('SELENIUM_URL', default).rstrip('/')

    def url(self, url_rule, *args, **kwargs):
        try:
            url = url_for(url_rule, *args, **kwargs)
        except BuildError:
            url = url_rule
        return self.host + url

    def test_index(self):
        index_url = self.url('index')

        self.browser.get(index_url)
        self.assertEqual(self.browser.current_url, index_url)
        time.sleep(1)

        element = self.browser.find_element_by_link_text('Learn Python')
        self.assertEqual(element.get_attribute('href'), index_url)

    def test_static(self):
        self.browser.get(self.url('static', filename='css/screen.css'))
        self.browser.get(self.url('static', filename='does_not_exists.exe'))
