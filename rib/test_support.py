import os
import contextlib
import tempfile
import shutil

import rib.app

@contextlib.contextmanager
def environment(**kwargs):
    original = os.environ.copy()

    for k, v in kwargs.items():
        if v is None:
            try:
                del os.environ[k]
            except KeyError:
                pass
        else:
            os.environ[k] = v

    yield

    for k, v in kwargs.items():
        if v is None:
            continue

        del os.environ[k]

    for k, v in original.items():
        os.environ[k] = v

@contextlib.contextmanager
def temp_path():
    path = tempfile.mkdtemp()

    original_wd = os.getcwd()
    os.chdir(path)

    yield path

    os.chdir(original_wd)

    if os.path.exists(path) is True:
        shutil.rmtree(path)

def get_test_client():
    app = rib.app.APP.test_client()
    return app
