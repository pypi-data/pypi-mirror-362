import os
import tempfile
from syncloudlib.integration.hosts import add_host_alias


def test_add_host_alias():

    fd, path = tempfile.mkstemp()
    try:
        add_host_alias('app', 'localhost', 'example.com', path)
        with os.fdopen(fd, 'r') as tmp:
            content = tmp.readlines()
            assert content[0].endswith(' example.com\n')
            assert content[1].endswith(' app.example.com\n')
    finally:
        os.remove(path)
    
