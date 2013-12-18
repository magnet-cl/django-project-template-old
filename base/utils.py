""" Small methods for generic use """

# standard library
import itertools


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.izip_longest(
        *args
    ))
