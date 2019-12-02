import pytest
from requests_html import HTMLSession

from eureka_inspect_cli.main import (parse_eureka_info)

session = HTMLSession()
session.mount('file://', FileAdapter())

def get():
    path = os.path.sep.join((os.path.dirname(os.path.abspath(__file__)), 'test.html'))
    url = 'file://{}'.format(path)

    return session.get(url)

def test_display():
    """Test """
    r = get()
    parsed = parse_eureka_info(r)
