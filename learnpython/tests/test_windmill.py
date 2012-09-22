from unittest import TestCase

from windmill.authoring import WindmillTestClient, setup_module, \
    teardown_module

from learnpython.app import app


class TestViewsWithWindmill(TestCase):

    def setUp(self):
        app.testing = True
        self.client = WindmillTestClient(__name__)
        self._ctx = app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    def test_index(self):
        self.client.open()
