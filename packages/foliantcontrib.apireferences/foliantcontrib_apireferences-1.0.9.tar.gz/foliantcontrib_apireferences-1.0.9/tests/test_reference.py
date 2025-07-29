import re

from foliant.preprocessors.apireferences.apireferences import DEFAULT_REF_REGEX
from foliant.preprocessors.apireferences.classes import Reference
from unittest import TestCase


class TestReference(TestCase):
    def test_repr_doesnt_throw_errors(self):
        ref = Reference(
            source='`MyAPI: GET /user/status`',
            prefix='MyAPI',
            verb='GET',
            command='/user/status'
        )
        ref.__repr__

    def test_init_from_match(self):
        source = '`MyAPI: GET /user/status`'
        pattern = re.compile(DEFAULT_REF_REGEX)
        match = pattern.search(source)
        ref = Reference()
        ref.init_from_match(match)
        self.assertEqual(ref.source, source)
        self.assertEqual(ref.prefix, 'MyAPI')
        self.assertEqual(ref.verb, 'GET')
        self.assertEqual(ref.command, '/user/status')

    def test_command_and_ep_slashes(self):
        ref = Reference(
            source='`MyAPI: GET /user/status`',
            prefix='MyAPI',
            verb='GET',
            command='user/status'
        )
        self.assertEqual(ref.command, '/user/status')

        ref = Reference(
            source='`MyAPI: GET /user/status`',
            prefix='MyAPI',
            verb='GET',
            command='api/v2/user/status',
            endpoint_prefix='/api/v2'
        )
        self.assertEqual(ref.command, '/user/status')

    def test_set_ep(self):
        ref = Reference(
            source='`MyAPI: GET /user/status`',
            prefix='MyAPI',
            verb='GET',
            command='/api/v2/user/status',
        )
        self.assertEqual(ref.command, '/api/v2/user/status')

        ref.endpoint_prefix = 'api/v2'
        self.assertEqual(ref.command, '/user/status')

    def test_fix_command(self):
        command = '/api/v2/user/status'
        command_without_ep = '/user/status'
        ep = '/api/v2'
        ref = Reference(command=command, endpoint_prefix=ep)
        self.assertEqual(ref.command, command_without_ep)
        self.assertEqual(ref.endpoint_prefix, ep)

        ref._fix_command()
        self.assertEqual(ref.command, command_without_ep)
        self.assertEqual(ref.endpoint_prefix, ep)

        ref = Reference(command=command)
        self.assertEqual(ref.command, command)
        self.assertEqual(ref.endpoint_prefix, '')

        ref._fix_command()
        self.assertEqual(ref.command, command)
        self.assertEqual(ref.endpoint_prefix, '')

    def test_setattr(self):
        command = '/api/v2/user/status'
        command_without_ep = '/user/status'
        ep = '/api/v2'
        ref = Reference(command=command)
        self.assertEqual(ref.command, command)

        ref.endpoint_prefix = ep
        self.assertEqual(ref.command, command_without_ep)
        self.assertEqual(ref.endpoint_prefix, ep)

        command2 = '/admin/sync'
        ref.command = command2
        self.assertEqual(ref.command, command2)
        self.assertEqual(ref.endpoint_prefix, ep)

        command3 = '/api/v2/user/logout'
        ref.command = command3
        self.assertEqual(ref.command, '/user/logout')
        self.assertEqual(ref.endpoint_prefix, ep)

    def test_custom_fields(self):
        ref = Reference(foo='foo', bar='bar')
        ref.endpoint_prefix = '/api/v2'
        self.assertEqual(ref.foo, 'foo')
        self.assertEqual(ref.bar, 'bar')
        self.assertEqual(ref.endpoint_prefix, '/api/v2')

    def test_dont_fix_empty_values(self):
        ref = Reference(foo='foo', command='bar')
        self.assertEqual(ref.endpoint_prefix, '')
        ref.command = ''
        self.assertEqual(ref.endpoint_prefix, '')
        self.assertEqual(ref.command, '')
