import os

from foliant.preprocessors.apireferences.classes import BadConfigError
from foliant.preprocessors.apireferences.classes import WrongModeError
from foliant.preprocessors.apireferences.classes import get_api
from unittest import TestCase

def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


class TestGetApi(TestCase):
    def test_get_api(self):
        options = {
            'mode': 'find_by_tag_content',
            'name': 'MyAPI',
            'url': 'https://example.com',
            'multiproject': False,
            'content_template': '{command}'
        }
        api = get_api(options)
        self.assertEqual(api.__class__.__name__, 'APIByTagContent')

        options = {
            'mode': 'generate_anchor',
            'name': 'MyAPI',
            'url': 'https://example.com',
            'multiproject': False,
            'anchor_template': '{command}'
        }
        api = get_api(options)
        self.assertEqual(api.__class__.__name__, 'APIGenAnchor')

        options = {
            'mode': 'find_by_anchor',
            'name': 'MyAPI',
            'url': 'https://example.com',
            'multiproject': False,
            'anchor_template': '{command}',
        }
        api = get_api(options)
        self.assertEqual(api.__class__.__name__, 'APIByAnchor')

        options = {
            'mode': 'find_for_swagger',
            'name': 'MyAPI',
            'url': 'https://example.com',
            'multiproject': False,
            'spec': rel_name('data/swagger.json')
        }
        api = get_api(options)
        self.assertEqual(api.__class__.__name__, 'APIBySwagger')

        options = {
            'mode': 'find_for_redoc',
            'name': 'MyAPI',
            'url': 'https://example.com',
            'multiproject': False,
            'spec': rel_name('data/swagger.json')
        }
        api = get_api(options)
        self.assertEqual(api.__class__.__name__, 'APIForRedoc')

    def test_missing_params(self):
        options = {
            'mode': 'find_by_tag_content',
            'name': 'MyAPI',
            'url': 'https://example.com',
        }
        with self.assertRaises(BadConfigError):
            get_api(options)

        options = {
            'mode': 'find_by_anchor',
            'name': 'MyAPI',
            'url': 'https://example.com',
        }
        with self.assertRaises(BadConfigError):
            get_api(options)

    def test_wrong_api(self):
        with self.assertRaises(WrongModeError):
            options = {
                'mode': 'wrong_mode',
                'name': 'MyAPI',
                'url': 'https://example.com',
            }
            get_api(options)

    def test_endpoint_prefix_max_endpoint_prefix_conflict(self):
        with self.assertRaises(BadConfigError):
            options = {
                'mode': 'find_by_tag_content',
                'name': 'MyApi',
                'url': 'http://example.com/',
                'multiproject': False,
                'content_template': '{verb} {command}',
                'endpoint_prefix': '/v2/',
                'max_endpoint_prefix': True
            }
            get_api(options)

    def test_endpoint_prefix_max_empty_endpoint_prefix_list(self):
        with self.assertRaises(BadConfigError):
            options = {
                'mode': 'find_by_tag_content',
                'name': 'MyApi',
                'url': 'http://example.com/',
                'multiproject': False,
                'content_template': '{verb} {command}',
                'endpoint_prefix_list': [],
                'max_endpoint_prefix': True
            }
            get_api(options)

    def test_endpoint_prefix_max_without_endpoint_prefix_list(self):
        with self.assertRaises(BadConfigError):
            options = {
                'mode': 'find_by_tag_content',
                'name': 'MyApi',
                'url': 'http://example.com/',
                'multiproject': False,
                'content_template': '{verb} {command}',
                'max_endpoint_prefix': True
            }
            get_api(options)
