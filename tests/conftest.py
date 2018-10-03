from os import chdir
from tempfile import mkdtemp

from pytest import fixture


@fixture
def clean_dir():
    new_path = mkdtemp()
    chdir(new_path)
