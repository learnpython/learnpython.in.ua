from learnpython.app import pages

from .common import TestCase


class TestData(TestCase):

    def check_flow(self, name, archive=False):
        prefix = 'flows' if not archive else 'archive/{0}'.format(archive)
        fullname = '{0}/{1}'.format(prefix, name)
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

    def test_archive(self):
        data = filter(lambda page: page.path.startswith('archive/1'), pages)
        self.assertEqual(len(data), 2)

    def test_flows(self):
        data = filter(lambda page: page.path.startswith('flows/'), pages)
        self.assertEqual(len(data), 3)

        self.check_flow('async')
        self.check_flow('optimization')
        self.check_flow('web')

    def test_pages(self):
        data = filter(lambda page: not '/' in page.path, pages)
        self.assertEqual(len(data), 6)

        self.check_page('about')
        self.check_page('archive')
        self.check_page('contacts')
        self.check_page('index')
        self.check_page('subscribe')
