# -*- coding: utf-8 -*-

from random import choice

from learnpython.app import pages
from learnpython.forms import FLOW_CHOICES

from .common import TEST_COMMENTS, TEST_EMAIL, TEST_NAME, TEST_MESSAGE, \
    TEST_PHONE, TEST_SUBJECT, TestCase


class TestViewsWithWebTest(TestCase):

    def assertRedirects(self, response, location):
        location = ':80{0}'.format(location)
        super(TestViewsWithWebTest, self).assertRedirects(response, location)

    def check_form_errors(self, url, collection):
        response = self.webtest.get(url)

        for data in collection:
            error = data.pop('error', 'This field is required.')
            form = response.form

            for key, value in data.items():
                form[key] = value

            response = form.submit()
            self.assert200(response)
            self.assertTrue(response.pyquery('form > p.error'))
            self.assertTrue(response.pyquery('form > p.error-line'))
            response.mustcontain(
                'Cannot submit form! Please, fix errors below:'
            )
            response.mustcontain(error)

    def check_form_success(self, url, collection, subject):
        for data in collection:
            response = self.webtest.get(url)
            form = response.form
            subject = data.get('subject', subject)

            for key, value in data.items():
                form[key] = value

            with self.mail.record_messages() as outbox:
                response = form.submit()
                self.assertStatus(response, 302)
                self.assertIn(self.status_url, response.headers['Location'])

                args = [data.pop('name'), data.pop('email')]
                data.pop('subject', None)
                args.extend(data.values())

                self.assertEqual(len(outbox), 1)
                self.check_message(outbox[0], subject, *args)

    def check_links(self, links, result):
        self.assertEqual(len(links), len(result))

        for i, link in enumerate(links):
            href, text = result[i]
            self.assertEqual(link.attrib['href'], href)
            self.assertEqual(link.text, text)

    def check_page(self, name, url):
        page = pages.get(name)
        self.assertIsNotNone(page)

        response = self.webtest.get(url, status=200)
        self.assertEqual(response.pyquery('article h2').text(),
                         page['title'])

    def test_about(self):
        self.check_page('about', self.about_url)

    def test_contacts(self):
        self.check_page('contacts', self.contacts_url)

        collection = (
            {},
            {'name': '', 'email': TEST_EMAIL, 'message': TEST_MESSAGE},
            {'name': TEST_NAME, 'email': '', 'message': TEST_MESSAGE},
            {'name': TEST_NAME, 'email': TEST_EMAIL, 'message': ''},
            {'name': TEST_NAME, 'email': TEST_NAME, 'message': TEST_MESSAGE,
             'error': 'Invalid email address.'},
        )
        self.check_form_errors(self.contacts_url, collection)

        collection = (
            {'name': TEST_NAME, 'email': TEST_EMAIL, 'message': TEST_MESSAGE},
            {'name': TEST_NAME, 'email': TEST_EMAIL, 'subject': TEST_SUBJECT,
             'message': TEST_MESSAGE},
        )
        self.check_form_success(self.contacts_url, collection, 'Feedback')

    def test_flows(self):
        flows = filter(lambda item: item[0].startswith('flows/'),
                       pages._pages.items())
        response = self.webtest.get(self.flows_url, status=200)
        doc = response.pyquery

        for fullname, flow in flows:
            name = fullname.replace('flows/', '')

            elements = doc('#{0}'.format(name))
            self.assertTrue(elements)
            self.assertEqual(len(elements), 1)

            element = elements[0]
            method = self.assertIn if flow['active'] else self.assertNotIn
            method('active', element.attrib['class'])

    def test_index(self):
        self.check_page('index', self.index_url)

        response = self.webtest.get(self.index_url)
        doc = response.pyquery

        self.assertEqual(len(doc('a.active')), 1)
        self.assertEqual(len(doc('a[href="{0}"]'.format(self.about_url))), 2)
        self.assertEqual(
            len(doc('a[href="{0}"]'.format(self.contacts_url))), 3
        )
        self.assertEqual(len(doc('a[href="{0}"]'.format(self.flows_url))), 0)
        self.assertEqual(len(doc('a[href="{0}"]'.format(self.index_url))), 1)
        self.assertEqual(
            len(doc('a[href="{0}"]'.format(self.subscribe_url))), 3
        )

        result = (
            (self.about_url, 'About us'),
            (self.contacts_url, 'Contacts')
        )
        self.check_links(doc('header .left-wrapper p a'), result)

        result = (
            (self.flows_url + '#medium', 'Medium flow'),
            (self.flows_url + '#normal', 'Normal flow'),
            (self.flows_url + '#advanced', 'Advanced flow'),
            (self.subscribe_url, u'Subscribe →'),
        )
        self.check_links(doc('nav a'), result)

    def test_static(self):
        url = self.url('static', filename='css/screen.css')
        response = self.webtest.get(url, status=200)

        url = self.url('static', filename='does_not_exist.exe')
        response = self.webtest.get(url, status=404)

    def test_subscribe(self):
        self.check_page('subscribe', self.subscribe_url)

        flow = choice(FLOW_CHOICES)[0]
        collection = (
            {},
            {'name': '', 'email': TEST_EMAIL, 'flow': flow},
            {'name': TEST_NAME, 'email': '', 'flow': flow},
            {'name': TEST_NAME, 'email': TEST_NAME, 'flow': flow,
             'error': 'Invalid email address.'},
        )
        self.check_form_errors(self.subscribe_url, collection)

        collection = (
            {'name': TEST_NAME, 'email': TEST_EMAIL, 'flow': flow},
            {'name': TEST_NAME, 'email': TEST_EMAIL, 'phone': TEST_PHONE,
             'flow': flow, 'comments': TEST_COMMENTS}
        )
        self.check_form_success(self.subscribe_url, collection, 'Subscribe')
