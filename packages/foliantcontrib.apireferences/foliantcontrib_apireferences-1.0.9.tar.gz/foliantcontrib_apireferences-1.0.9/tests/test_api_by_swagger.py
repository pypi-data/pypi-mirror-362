import os

from foliant.preprocessors.apireferences.classes import APIBySwagger
from foliant.preprocessors.apireferences.classes import Reference
from foliant.preprocessors.apireferences.classes import ReferenceNotFoundError
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch


def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


class TestAPIBySwagger(TestCase):
    def test_generate_registry_url(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            mock_read = Mock()
            with open(rel_name('data/swagger.json'), 'rb') as f:
                mock_read.read.return_value = f.read()
            mock_urlopen.return_value = mock_read
            api = APIBySwagger(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                spec='http://example.com/test.json',
                anchor_template='/{tag}/{operation_id}',
            )
            self.assertTrue(mock_urlopen.called)

        expected_registry = {
            'POST /pet': {
                'tag': 'pettag',
                'operation_id': 'addPet'
            },
            'PUT /pet': {
                'tag': 'pettag',
                'operation_id': 'updatePet'
            },
            'GET /api/v2/pet/findByStatus': {
                'tag': 'pettag',
                'operation_id': 'findPetsByStatus'
            }
        }
        self.assertEqual(api.registry, expected_registry)

    def test_generate_registry_url_with_credentials(self):
        with patch('foliant.preprocessors.apireferences.classes.urlopen_with_auth') as mock_urlopen:
            with open(rel_name('data/swagger.json'), 'rb') as f:
                mock_urlopen.return_value = f.read()
            api = APIBySwagger(
                name='Test',
                url='http://example.com/',
                multiproject=False,
                spec='http://example.com/test.json',
                anchor_template='/{tag}/{operation_id}',
                login='login',
                password='password'
            )
            self.assertTrue(mock_urlopen.called)

        expected_registry = {
            'POST /pet': {
                'tag': 'pettag',
                'operation_id': 'addPet'
            },
            'PUT /pet': {
                'tag': 'pettag',
                'operation_id': 'updatePet'
            },
            'GET /api/v2/pet/findByStatus': {
                'tag': 'pettag',
                'operation_id': 'findPetsByStatus'
            }
        }
        self.assertEqual(api.registry, expected_registry)

    def test_generate_registry_path(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
        )

        expected_registry = {
            'POST /pet': {
                'tag': 'pettag',
                'operation_id': 'addPet'
            },
            'PUT /pet': {
                'tag': 'pettag',
                'operation_id': 'updatePet'
            },
            'GET /api/v2/pet/findByStatus': {
                'tag': 'pettag',
                'operation_id': 'findPetsByStatus'
            }
        }
        self.assertEqual(api.registry, expected_registry)

    def test_get_extended_reference(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
        )

        ref = Reference(verb='PUT', command='/pet')
        ext_ref = api.get_extended_reference(ref)
        expected_ref = Reference(tag='pettag', operation_id='updatePet', **ref.__dict__)
        self.assertEqual(ext_ref.__dict__, expected_ref.__dict__)

    def test_get_extended_reference_with_ep(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
            endpoint_prefix='/api/v2'
        )

        ref = Reference(verb='PUT', command='/pet')
        ext_ref = api.get_extended_reference(ref)
        expected_ref = Reference(tag='pettag', operation_id='updatePet', **ref.__dict__)
        expected_ref.__dict__['endpoint_prefix'] = '/api/v2'
        self.assertEqual(ext_ref.__dict__, expected_ref.__dict__)
        self.assertEqual(ref.endpoint_prefix, '')
        self.assertNotIn('tag', ref.__dict__)

        ref = Reference(verb='PUT', command='/api/v2/pet')
        ext_ref = api.get_extended_reference(ref)
        self.assertEqual(ext_ref.__dict__, expected_ref.__dict__)

        ref = Reference(verb='GET', command='/pet/findByStatus')
        ext_ref = api.get_extended_reference(ref)
        expected_ref = Reference(tag='pettag', operation_id='findPetsByStatus', **ref.__dict__)
        expected_ref.__dict__['endpoint_prefix'] = '/api/v2'
        self.assertEqual(ext_ref.__dict__, expected_ref.__dict__)

        ref = Reference(verb='GET', command='/api/v2/pet/findByStatus')
        ext_ref = api.get_extended_reference(ref)
        self.assertEqual(ext_ref.__dict__, expected_ref.__dict__)

    def test_get_extended_reference_not_found(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
        )

        ref = Reference(verb='GET', command='/wrong/path')
        with self.assertRaises(ReferenceNotFoundError):
            api.get_extended_reference(ref)

    def test_get_anchor_by_reference(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
        )

        ref = Reference(verb='PUT', command='/pet')
        expected_anchor = '/pettag/updatePet'
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, expected_anchor)

    def test_get_anchor_by_reference_with_query(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{tag}/{operation_id}',
        )

        ref = Reference(verb='PUT', command='/pet?spieces=cat,dog')
        expected_anchor = '/pettag/updatePet'
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, expected_anchor)

    def test_get_anchor_by_reference_custom_template(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{verb}/{operation_id}/{command}',
        )

        ref = Reference(verb='PUT', command='/pet')
        expected_anchor = '/PUT/updatePet//pet'
        anchor = api.get_anchor_by_reference(ref)
        self.assertEqual(anchor, expected_anchor)

    def test_check_reference(self):
        api = APIBySwagger(
            name='Test',
            url='http://example.com/',
            multiproject=False,
            spec=rel_name('data/swagger.json'),
            anchor_template='/{foo}/{operation_id}/{command}',
        )
        ref = Reference(foo='foo')
        api.check_reference(ref)

        ref = Reference(bar='bar')
        with self.assertRaises(ReferenceNotFoundError):
            api.check_reference(ref)
