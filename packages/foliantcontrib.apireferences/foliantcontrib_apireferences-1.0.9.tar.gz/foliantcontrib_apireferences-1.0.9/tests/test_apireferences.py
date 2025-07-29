import io
import logging
import os
import sys

from foliant.preprocessors.apireferences.classes import HTTP_VERBS
from foliant.preprocessors.apireferences.apireferences import DEFAULT_REF_REGEX
from foliant_test.preprocessor import PreprocessorTestFramework
from foliant_test.preprocessor import unpack_dir
from foliant_test.preprocessor import unpack_file_dict
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch


logging.basicConfig(
    filename='test.log',
    # encoding='utf-8',
    level=logging.DEBUG,
)


def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


def count_output_warnings(source) -> int:
    return source.getvalue().lower().count('warning')


class TestAPIReferences(TestCase):
    def setUp(self):
        self.ptf = PreprocessorTestFramework('apireferences')
        self.ptf.quiet = False
        self.ptf.capturedOutput = io.StringIO()
        sys.stdout = self.ptf.capturedOutput

    def run_with_mock_url(self, source_file, **kwargs):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            with open(rel_name(source_file), 'rb') as f:
                mock_read = Mock()
                mock_read.read.return_value = f.read()
                mock_urlopen.return_value = mock_read
                self.ptf.test_preprocessor(**kwargs)

    def run_with_mock_urls(self, source_files, **kwargs):
        with patch('foliant.preprocessors.apireferences.classes.urlopen') as mock_urlopen:
            sources = []
            for file in source_files:
                with open(rel_name(file), 'rb') as f:
                    sources.append(f.read())

            mock_read = Mock()
            mock_read.read.side_effect = sources
            mock_urlopen.return_value = mock_read
            self.ptf.test_preprocessor(**kwargs)

    def test_simple_h2h3_by_content(self):
        self.ptf.options = {
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'multiproject': False,
                    'mode': 'find_by_tag_content',
                    'content_template': '{verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping=unpack_file_dict(
                {'single_h2h3.md': rel_name('data/input/single_h2h3.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_h2h3.md': rel_name('data/expected/single_h2h3.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_simple_h2h3_by_anchor(self):
        self.ptf.options = {
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping=unpack_file_dict(
                {'single_h2h3.md': rel_name('data/input/single_h2h3.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_h2h3.md': rel_name('data/expected/single_h2h3.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_simple_a_by_content(self):
        self.ptf.options = {
            'API': {
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_tag_content',
                    'content_template': '{verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.run_with_mock_url(
            'data/simple_a.html',
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/expected/single_a.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_simple_a_by_anchor(self):
        self.ptf.options = {
            'API': {
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'puppy content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.run_with_mock_url(
            'data/simple_a.html',
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/expected/single_a.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_gen_anchor(self):
        self.ptf.options = {
            'API': {
                'Gen-Api': {
                    'url': 'http://example.com/',
                    'mode': 'generate_anchor',
                    'multiproject': False,
                    'anchor_template': '{verb} {command}',
                }
            }
        }
        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'gen_anchor.md': rel_name('data/input/gen_anchor.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'gen_anchor.md': rel_name('data/expected/gen_anchor.md')}
            ),
        )

        self.assertEqual(1, count_output_warnings(self.ptf.capturedOutput))

    def test_gen_anchor_wrong_groups(self):
        self.ptf.options = {
            'API': {
                'Gen-Api': {
                    'url': 'http://example.com/',
                    'mode': 'generate_anchor',
                    'multiproject': False,
                    'anchor_template': '{foo} {bar}',
                }
            }
        }
        self.ptf.test_preprocessor(
            input_mapping={
                'gen_anchor.md': 'My reference `Gen-API: GET /test`.'
            },
            expected_mapping={
                'gen_anchor.md': 'My reference `Gen-API: GET /test`.'
            },
        )

        self.assertEqual(1, count_output_warnings(self.ptf.capturedOutput))

    def test_swagger(self):
        self.ptf.options = {
            'API': {
                'Swagger-API': {
                    'url': 'http://example.com/',
                    'mode': 'find_for_swagger',
                    'spec': rel_name('data/swagger.json'),
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'single_swagger.md': rel_name('data/input/single_swagger.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_swagger.md': rel_name('data/expected/single_swagger.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_faulty(self):
        self.ptf.options = {
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                },
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'puppy content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_urls(
            ('data/simple_h2h3.html', 'data/simple_a.html'),
            input_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/input/faulty.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/expected/faulty.md')}
            ),
        )

        self.assertEqual(4, count_output_warnings(self.ptf.capturedOutput))

    def test_all_at_once(self):
        self.ptf.options = {
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                },
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'puppy content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                },
                'Swagger-API': {
                    'url': 'http://example.com/',
                    'multiproject': False,
                    'mode': 'find_for_swagger',
                    'spec': rel_name('data/swagger.json'),
                    'endpoint_prefix': '/api/v2'
                },
                'Gen-Api': {
                    'url': 'http://example.com/',
                    'multiproject': False,
                    'mode': 'generate_anchor',
                    'anchor_template': '{verb} {command}',
                }
            }
        }
        self.run_with_mock_urls(
            ('data/simple_h2h3.html', 'data/simple_a.html'),
            input_mapping=unpack_file_dict(
                {
                    'faulty.md': rel_name('data/input/faulty.md'),
                    'gen_anchor.md': rel_name('data/input/gen_anchor.md'),
                    'single_a.md': rel_name('data/input/single_a.md'),
                    'single_h2h3.md': rel_name('data/input/single_h2h3.md'),
                    'single_swagger.md': rel_name('data/input/single_swagger.md'),
                }
            ),
            expected_mapping=unpack_dir(rel_name('data/expected_all_at_once')),
        )

        self.assertEqual(11, count_output_warnings(self.ptf.capturedOutput))

    def test_single_a_and_trim(self):
        self.ptf.options = {
            'trim_if_targets': ['pre'],
            'reference': [
                {'trim_template': '**{verb} {command}**'}
            ],
            'API': {
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_tag_content',
                    'content_template': '{verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.ptf.context['target'] = 'pre'
        self.run_with_mock_url(
            'data/simple_a.html',
            input_mapping=unpack_file_dict(
                {'single_a_and_trim.md': rel_name('data/input/single_a_and_trim.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a_and_trim.md': rel_name('data/expected/single_a_and_trim.md')}
            ),
        )

        self.assertEqual(1, count_output_warnings(self.ptf.capturedOutput))

    def test_simple_a_only_trim(self):
        self.ptf.options = {
            'trim_if_targets': ['pre'],
            'targets': ['pdf'],
            'API': {
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_tag_content',
                    'content_template': '{verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.ptf.context['target'] = 'pre'

        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/expected/single_a_only_trim.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_only_with_prefixes_nothing_to_do(self):
        self.ptf.options = {
            'reference': [
                {'only_with_prefixes': True}
            ],
            'API': {
                'Swagger-API': {
                    'url': 'http://example.com/',
                    'mode': 'find_for_swagger',
                    'spec': rel_name('data/swagger.json'),
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
        )
        self.assertEqual(3, count_output_warnings(self.ptf.capturedOutput))

    def test_only_with_defined_prefixes_nothing_to_do(self):
        self.ptf.options = {
            'reference': [
                {
                    'only_with_prefixes': True,
                    'only_defined_prefixes': True,
                }
            ],
            'API': {
                'Swagger-API': {
                    'url': 'http://example.com/',
                    'mode': 'find_for_swagger',
                    'spec': rel_name('data/swagger.json'),
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_only_with_prefixes_trim_nothing_to_do(self):
        self.ptf.options = {
            'trim_if_targets': ['pre'],
            'targets': ['pdf'],
            'reference': [
                {'only_with_prefixes': True}
            ],
            'API': {
                'Swagger-API': {
                    'url': 'http://example.com/',
                    'mode': 'find_for_swagger',
                    'spec': rel_name('data/swagger.json'),
                    'endpoint_prefix': '/api/v2'
                }
            }
        }
        self.ptf.context['target'] = 'pre'

        self.ptf.test_preprocessor(
            input_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'single_a.md': rel_name('data/input/single_a.md')}
            ),
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_reference_custom_output_template(self):
        self.ptf.options = {
            'reference': [
                {'output_template': '**Command {command} ({verb})**'}
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': 'My reference: `GET /user/login`.'
            },
            expected_mapping={
                'input.md': 'My reference: **Command /user/login (GET)**.'
            }
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_reference_custom_regex(self):
        pattern = rf'!!!(?P<verb>{"|".join(HTTP_VERBS)})\s*(?P<command>.+?)!!!'
        self.ptf.options = {
            'reference': [
                {
                    'regex': pattern
                }
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': 'My reference: !!!GET /user/login!!!.'
            },
            expected_mapping={
                'input.md': 'My reference: [GET /user/login](http://example.com/#user-content-get-userlogin).'
            }
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_reference_custom_regex_output(self):
        pattern = rf'!!!(?P<myverb>{"|".join(HTTP_VERBS)})\s*(?P<mycommand>.+?)!!!'
        self.ptf.options = {
            'reference': [
                {
                    'regex': pattern,
                    'output_template': '**Command {mycommand} ({myverb})**'
                }
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {myverb} {mycommand}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': 'My reference: !!!GET /user/login!!!.'
            },
            expected_mapping={
                'input.md': 'My reference: **Command /user/login (GET)**.'
            }
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_several_references(self):
        pattern = rf'!!!(?P<verb>{"|".join(HTTP_VERBS)})\s*(?P<command>.+?)!!!'
        self.ptf.options = {
            'reference': [
                {
                    'regex': pattern,
                    'output_template': '**Command {command} ({verb})**'
                },
                {
                    'only_with_prefixes': True,
                }
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': 'My reference: !!!GET /user/login!!!. My another reference: `H2H3-Api: GET system/restart`.'
            },
            expected_mapping={
                'input.md': 'My reference: **Command /user/login (GET)**. My another reference: [GET /system/restart](http://example.com/#user-content-get-systemrestart).'
            }
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_counters(self):
        self.ptf.options = {
            'API': {
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'puppy content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url('data/simple_a.html',
            input_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/input/faulty.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/expected/half_faulty.md')}
            ),
        )

        self.assertEqual(3, count_output_warnings(self.ptf.capturedOutput))
        self.assertIn('1 links added, 3 links skipped.', self.ptf.capturedOutput.getvalue())

    def test_warning_level(self):
        self.ptf.options = {
            'warning_level': 2,
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                },
                'A-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'puppy content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_urls(
            ('data/simple_h2h3.html', 'data/simple_a.html'),
            input_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/input/faulty.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/expected/faulty.md')}
            ),
        )
        self.assertEqual(4, count_output_warnings(self.ptf.capturedOutput))

        self.ptf.capturedOutput.truncate(0)
        self.ptf.options['warning_level'] = 1
        self.run_with_mock_urls(
            ('data/simple_h2h3.html', 'data/simple_a.html'),
            input_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/input/faulty.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/expected/faulty.md')}
            ),
        )

        self.assertEqual(1, count_output_warnings(self.ptf.capturedOutput))

        self.ptf.capturedOutput.truncate(0)
        self.ptf.options['warning_level'] = 0
        self.run_with_mock_urls(
            ('data/simple_h2h3.html', 'data/simple_a.html'),
            input_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/input/faulty.md')}
            ),
            expected_mapping=unpack_file_dict(
                {'faulty.md': rel_name('data/expected/faulty.md')}
            ),
        )

        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_reference_with_backtick_spaces(self):
        pattern = DEFAULT_REF_REGEX
        self.ptf.options = {
            'reference': [
                {
                    'regex': pattern
                }
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': '` GET /user/login `'
            },
            expected_mapping={
                'input.md': '[GET /user/login](http://example.com/#user-content-get-userlogin)'
            }
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))

    def test_reference_with_backtick_spaces_as_a_list_item(self):
        pattern = DEFAULT_REF_REGEX
        self.ptf.options = {
            'reference': [
                {
                    'regex': pattern
                }
            ],
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.run_with_mock_url(
            'data/simple_h2h3.html',
            input_mapping={
                'input.md': '- ` GET /user/login `'
            },
            expected_mapping={
                'input.md': '- [GET /user/login](http://example.com/#user-content-get-userlogin)'
            }
        )
        self.assertEqual(0, count_output_warnings(self.ptf.capturedOutput))