import pytest
import os

from eureka_inspect_cli.main import (parse_eureka_info)

def get():
    path = os.path.sep.join((os.path.dirname(os.path.abspath(__file__)), 'test.html'))
    f = open(path, 'r')
    html = f.read()

    return html

def test_parse():
    """Test """
    r = get()
    parsed = parse_eureka_info(r)
    assert len(parsed) == 3
    assert parsed[0].name == 'APP-1'
    assert parsed[0].up_instances == ['192.168.1.99:1408', '192.168.1.99:4839', '192.168.1.99:2898']
    assert parsed[0].down_instances == ['192.168.1.99:1136']
