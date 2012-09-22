from flask import url_for
from flask.ext.testing import TestCase
from webtest import TestApp

from learnpython.app import app


class TestViews(TestCase):

    def assertRedirects(self, response, location):
        location = ':80{0}'.format(location)
        super(TestViews, self).assertRedirects(response, location)

    def create_app(self):
        app.testing = True
        self.webtest = TestApp(app)
        return app

    def test_index(self):
        index_url = url_for('page', name='index')

        response = self.webtest.get('/', status=301)
        self.assertRedirects(response, index_url)

        response = self.webtest.get(index_url)
        self.assert200(response)
        self.assertEqual(
            response.pyquery('a[href="{0}"]'.format(index_url)).text(),
            'Learn Python'
        )

    def test_static(self):
        url = url_for('static', filename='css/screen.css')
        response = self.webtest.get(url, status=200)

        url = url_for('static', filename='does_not_exist.exe')
        response = self.webtest.get(url, status=404)
