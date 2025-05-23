"""
Write a context manager, that suppresses passed exception.
Do it both ways: as a class and as a generator.

>>> with supressor(IndexError):
...    [][2]

"""
from contextlib import contextmanager


@contextmanager
def supressor(exception):
    try:
        yield
    except exception:
        pass