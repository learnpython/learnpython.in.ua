from learnpython.app import pages

from .common import TestCase


class TestData(TestCase):

    def check_flow(self, name):
        fullname = 'flows/{0}'.format(name)
        flow = self.check_page(fullname)
        self.assertIn('active', flow.meta)
        self.assertIn('order', flow.meta)

    def check_page(self, mixed):
        page = pages.get(mixed) if isinstance(mixed, basestring) else mixed
        self.assertIsNotNone(page)

        self.assertIn('title', page.meta)
        self.assertNotEqual(page.body, '')
        self.assertNotEqual(page.html, '')

        return page

    def test_flows(self):
        data = filter(lambda key: key.startswith('flows/'),
                      pages._pages.keys())
        self.assertEqual(len(data), 2)

        self.check_flow('advanced')
        self.check_flow('web')

    def test_pages(self):
        data = filter(lambda key: not '/' in key, pages._pages.keys())
        self.assertEqual(len(data), 4)

        self.check_page('about')
        self.check_page('contacts')
        self.check_page('index')
        self.check_page('subscribe')
