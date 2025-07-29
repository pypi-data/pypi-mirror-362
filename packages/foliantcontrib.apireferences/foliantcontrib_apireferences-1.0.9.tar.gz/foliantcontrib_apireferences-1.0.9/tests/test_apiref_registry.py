import json
import socket
import threading
import time
from unittest.mock import Mock, patch
from unittest import TestCase
from foliant_test.preprocessor import PreprocessorTestFramework
from http.server import SimpleHTTPRequestHandler, HTTPServer


class JsonHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "A-Api": [
                    "puppy-content-get-puppy"
                ],
                "H2H3-Api": [
                    "user-content-get-systemrestart",
                    "user-content-get-userlogin",
                ],
                "Swagger-API": [
                    "loginUser",
                    "restartSystem"
                ]
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


class ReusableHTTPServer(HTTPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()


class TestAPIRegistry(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = find_free_port()
        cls.server = ReusableHTTPServer(('', cls.port), JsonHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)  # Даем серверу время запуститься

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def setUp(self):
        self.ptf = PreprocessorTestFramework('apireferences')
        self.ptf.quiet = True

    def test_external_registry_loading(self):
        """Test loading the registry from an external URL"""
        self.ptf.options = {
            'apiref_registry_url': f'http://localhost:{self.port}/data.json',
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        self.ptf.test_preprocessor(
            input_mapping={
                'input.md': '`H2H3-Api: GET /user/login`'
            },
            expected_mapping={
                'input.md': '[GET /user/login](http://example.com/#user-content-get-userlogin)'
            }
        )

    def test_external_registry_fallback(self):
        """Fallback test for registry loading error"""
        self.ptf.options = {
            'apiref_registry_url': 'http://localhost:9999/nonexistent.json',
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        with self.assertRaises(Exception):
            self.ptf.test_preprocessor(
                input_mapping={
                    'input.md': '`H2H3-Api: GET /user/login`'
                }
            )

    def test_multiple_apis_with_registry(self):
        """The test of the operation of several APIs with a common registry"""
        self.ptf.options = {
            'apiref_registry_url': f'http://localhost:{self.port}/data.json',
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

        self.ptf.test_preprocessor(
            input_mapping={
                'input.md': '`H2H3-Api: GET /user/login` and `A-Api: GET /puppy`'
            },
            expected_mapping={
                'input.md': '[GET /user/login](http://example.com/#user-content-get-userlogin) and [GET /puppy](http://example.com/#puppy-content-get-puppy)'
            }
        )

    def test_registry_with_multiproject_mode(self):
        """The test of the registry operation in multiproject mode"""
        self.ptf.options = {
            'apiref_registry_url': f'http://localhost:{self.port}/data.json',
            'use_multiproject_mode': True,
            'API': {
                'H2H3-Api': {
                    'url': 'http://example.com/',
                    'mode': 'find_by_anchor',
                    'anchor_template': 'user content {verb} {command}',
                    'endpoint_prefix': '/api/v2'
                }
            }
        }

        with patch('os.path.join', return_value='../H2H3-Api.apirefregistry'):
            with patch('os.path.isfile', return_value=False):
                self.ptf.test_preprocessor(
                    input_mapping={
                        'input.md': '`H2H3-Api: GET /user/login`'
                    },
                    expected_mapping={
                        'input.md': '[GET /user/login](http://example.com/#user-content-get-userlogin)'
                    }
                )

    # def test_registry_with_swagger_api(self):
    #     self.ptf.options = {
    #         'apiref_registry_url': f'http://localhost:{self.port}/data.json',
    #         'API': {
    #             'Swagger-API': {
    #                 'url': 'http://example.com/',
    #                 'mode': 'find_for_swagger',
    #                 'spec': 'http://example.com/swagger.json',
    #                 'anchor_template': '/{tag}/{operation_id}',
    #                 'endpoint_prefix': '/api/v2'
    #             }
    #         }
    #     }

    #     self.ptf.test_preprocessor(
    #         input_mapping={
    #             'input.md': '`Swagger-API: GET /user/login`'
    #         },
    #         expected_mapping={
    #             'input.md': '[GET /user/login](http://example.com/#/user/loginUser)'
    #         }
    #     )

    def test_registry_with_generate_anchor_mode(self):
        """The test of how the registry works with the API in generate_anchor mode"""
        self.ptf.options = {
            'apiref_registry_url': f'http://localhost:{self.port}/data.json',
            'API': {
                'Gen-Api': {
                    'url': 'http://example.com/',
                    'mode': 'generate_anchor',
                    'anchor_template': '{verb} {command}'
                }
            }
        }

        self.ptf.test_preprocessor(
            input_mapping={
                'input.md': '`Gen-Api: GET /test`'
            },
            expected_mapping={
                'input.md': '[GET /test](http://example.com/#get-test)'
            }
        )
