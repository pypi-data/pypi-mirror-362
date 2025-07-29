import os

from foliant.preprocessors.apireferences.classes import APIByAnchor
from foliant.preprocessors.apireferences.classes import Reference
from foliant.preprocessors.apireferences.classes import ReferenceNotFoundError
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch


def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


class TestAPIByAnchor(TestCase):
    def test_generate_registry(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3']
            )
            self.assertTrue(mock_urlopen.called)

        expected_registry = [
            'user-content-get-apiv2adminstatus',
            'user-content-get-systemrestart',
            'user-content-get-systemstatus',
            'user-content-get-userlogin',
            'user-content-get-v1userinfo',
            'user-content-get-v2userinfo',
            'user-content-get-v3userinfo'
        ]
        self.assertEqual(api.registry, expected_registry)

    def test_generate_registry_another_tag(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_a.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='a {verb} {command}',
                tags=['a']
            )
            self.assertTrue(mock_urlopen.called)

        expected_registry = ['a-get-apiv2dogstatus',
                             'a-get-puppylogin',
                             'a-get-systemrestart']
        self.assertEqual(api.registry, expected_registry)

    def test_generate_registry_with_credentials(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen_with_auth') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_urlopen.return_value = f.read()
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3'],
                login='login',
                password='password'
            )
            self.assertTrue(mock_urlopen.called)

        expected_registry = [
            'user-content-get-apiv2adminstatus',
            'user-content-get-systemrestart',
            'user-content-get-systemstatus',
            'user-content-get-userlogin',
            'user-content-get-v1userinfo',
            'user-content-get-v2userinfo',
            'user-content-get-v3userinfo'
        ]
        self.assertEqual(api.registry, expected_registry)

    def get_basic_api(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            return APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3']
            )

    def test_generate_anchor_by_reference_without_ep(self):
        api = self.get_basic_api()
        ref = Reference(verb='GET', command='/user/login')
        content = api.generate_anchor_by_reference(ref, False)
        self.assertEqual(content, 'user-content-get-userlogin')
        content = api.generate_anchor_by_reference(ref, True)
        self.assertEqual(content, 'user-content-get-userlogin')

    def test_generate_anchor_by_reference_with_ep(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/user/login')
        content = api.generate_anchor_by_reference(ref, False)
        self.assertEqual(content, 'user-content-get-userlogin')
        content = api.generate_anchor_by_reference(ref, True)
        self.assertEqual(content, 'user-content-get-apiv2userlogin')
        self.assertEqual(ref.endpoint_prefix, '')

    def test_generate_anchor_by_reference_without_command(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        api.anchor_template = 'user content {verb} {foo}'
        ref = Reference(verb='GET', foo='/user/login')
        content = api.generate_anchor_by_reference(ref, False)
        self.assertEqual(content, 'user-content-get-userlogin')
        content = api.generate_anchor_by_reference(ref, True)
        self.assertEqual(content, 'user-content-get-userlogin')

    def test_generate_anchor_by_reference_slate_converter(self):
        api = self.get_basic_api()
        api.anchor_converter = 'slate'
        ref = Reference(verb='GET', command='/user/login')
        content = api.generate_anchor_by_reference(ref, False)
        self.assertEqual(content, 'user-content-get-user-login')
        content = api.generate_anchor_by_reference(ref, True)
        self.assertEqual(content, 'user-content-get-user-login')

    def test_get_anchor_by_reference(self):
        api = self.get_basic_api()
        ref = Reference(verb='GET', command='/user/login')
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-userlogin')

    def test_get_anchor_by_reference_with_prefix(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/admin/status')
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-apiv2adminstatus')

    def test_get_anchor_by_reference_with_extra_prefix(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/api/v2/system/restart')
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-systemrestart')

    def test_get_anchor_by_reference_custom_groups(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {foo} {bar}',
                tags=['h1', 'h2', 'h3']
            )
        api.endpoint_prefix = '/api/v2'
        ref = Reference(foo='GET', bar='/system/restart')
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, 'user-content-get-systemrestart')

    def test_get_nonexistant_anchor(self):
        api = self.get_basic_api()
        ref = Reference(verb='GET', command='/wrong/command')
        with self.assertRaises(ReferenceNotFoundError):
            api.get_anchor_by_reference(ref)

    def test_get_link_by_reference(self):
        api = self.get_basic_api()
        ref = Reference(verb='GET', command='/user/login')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-userlogin')

    def test_get_link_by_reference_with_prefix(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/admin/status')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-apiv2adminstatus')

    def test_get_link_by_reference_with_extra_prefix(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/api/v2/system/restart')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-systemrestart')

    def test_get_link_by_reference_with_query(self):
        api = self.get_basic_api()
        api.endpoint_prefix = '/api/v2'
        ref = Reference(verb='GET', command='/admin/status?users=guest,admin')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-apiv2adminstatus')

    def test_get_nonexistant_link(self):
        api = self.get_basic_api()
        ref = Reference(verb='GET', command='/wrong/command')
        with self.assertRaises(ReferenceNotFoundError):
            api.get_link_by_reference(ref)

    def test_check_reference(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command} {foo}',
                tags=['h1', 'h2', 'h3']
            )
        ref = Reference(foo='foo')
        api.check_reference(ref)

        ref = Reference(bar='bar')
        with self.assertRaises(ReferenceNotFoundError):
            api.check_reference(ref)

    def test_get_link_by_reference_max_version(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3'],
                max_endpoint_prefix=True,
                endpoint_prefix_list=['/v1/', '/v2/', '/v3/']
            )

        ref = Reference(verb='GET', command='/user/info')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-v3userinfo')

    def test_get_link_by_reference_max_version_with_explicit_prefix(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3'],
                max_endpoint_prefix=True,
                endpoint_prefix_list=['/v1/', '/v2/', '/v3/']
            )

        ref = Reference(verb='GET', command='/v1/user/info')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-v1userinfo')

    def test_get_link_by_reference_max_version_nonversioned(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name('data/simple_h2h3.html'), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
            api = APIByAnchor(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                anchor_template='user content {verb} {command}',
                tags=['h1', 'h2', 'h3'],
                max_endpoint_prefix=True,
                endpoint_prefix_list=['/v1/', '/v2/', '/v3/']
            )

        ref = Reference(verb='GET', command='/system/status')
        link = api.get_link_by_reference(ref)
        self.assertEqual(link, 'http://example.com/#user-content-get-systemstatus')