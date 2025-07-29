import os

from foliant.preprocessors.apireferences.classes import APIGenAnchor
from foliant.preprocessors.apireferences.classes import Reference
from unittest import TestCase


def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


class TestAPIGenAnchor(TestCase):
    def test_generate_anchor_by_reference(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='user content {verb} {command}',
        )
        ref = Reference(verb='GET', command='/user/info')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-userinfo')

    def test_generate_anchor_by_reference_with_query(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='user content {verb} {command}',
        )
        ref = Reference(verb='GET', command='/user/info?type=common,secret')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-userinfo')

    def test_generate_anchor_by_reference_custom_field(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='{foo} {verb} {command}',
        )
        ref = Reference(verb='GET', command='/user/info', foo='bar')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'bar-get-userinfo')

    def test_gerenate_anchor_by_reference_all_custom_groups(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='{foo} {bar} {baz}',
        )
        ref = Reference(foo='foo', bar='bar', baz='baz')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'foo-bar-baz')

    def test_generate_anchor_by_reference_with_ep(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='{verb} {endpoint_prefix}{command}',
            endpoint_prefix='/api/v2'
        )
        ref = Reference(verb='GET', command='/user/info', foo='bar')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'get-apiv2userinfo')

    def test_generate_anchor_by_reference_slate_converter(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='{verb} {command}',
            endpoint_prefix='/api/v2',
            anchor_converter='slate'
        )
        ref = Reference(verb='GET', command='/user/login')
        content = api.generate_anchor_by_reference(ref)
        self.assertEqual(content, 'get-user-login')

    def test_check_reference(self):
        api = APIGenAnchor(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            anchor_template='{foo} {bar} {baz}',
        )
        ref = Reference(foo='foo', bar='bar', baz='baz')
        anchor = api.generate_anchor_by_reference(ref)
        self.assertEqual(anchor, 'foo-bar-baz')
        ref = Reference(foo='foo', bar='bar', baz='baz')
        api.check_reference(ref)

        ref = Reference()
        with self.assertRaises(RuntimeError):
            api.check_reference(ref)
