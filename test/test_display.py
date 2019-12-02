import pytest
import os

from eureka_inspect_cli.main import (parse_eureka_info)

def get():
    path = os.path.sep.join((os.path.dirname(os.path.abspath(__file__)), 'test.html'))
    f = open(path, 'r')
    html = f.read()

    return html

def test_display():
    """Test """
    r = get()
    parsed = parse_eureka_info(r)
    for n in parsed:
        n.print()

if __name__ == '__main__':
    test_display()