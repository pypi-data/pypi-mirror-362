import base64

from urllib.request import Request
from urllib.request import urlopen


def ensure_root(route):
    '''ensure that route starts with forward slash. Also, trim trailing slash.'''
    if route:
        return '/' + route.strip('/ ')
    return route


def urlopen_with_auth(dest: str, login: str, password: str, context=None):
    request = Request(dest)
    b64_creds = base64.b64encode(bytes(f'{login}:{password}', 'ascii')).decode('utf-8')
    request.add_header('Authorization', f'Basic {b64_creds}')
    result = urlopen(request, context=context)
    return result.read()


def normalize_content(content: str) -> str:
    """
    Remove preceding and trailing whitespaces from `content` string.

    :param content: string to be normalized.

    :returns: normalized string.
    """

    return content.strip(' \n\t')
