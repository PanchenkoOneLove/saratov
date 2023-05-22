"""
Some of the functions have a bit cumbersome behavior when we deal with
positional and keyword arguments.
Write a function that accept any iterable of unique values and then
it behaves as range function:
import string
assert = custom_range(string.ascii_lowercase, 'g') == ['a', 'b', 'c', 'd', 'e', 'f']
assert = custom_range(string.ascii_lowercase, 'g', 'p') == ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
assert = custom_range(string.ascii_lowercase, 'p', 'g', -2) == ['p', 'n', 'l', 'j', 'h']
"""
import string


def custom_range(iterable, start, stop=None, step=1):
    if not stop:
        stop = start
        start = 0
        result = []
        i = 0
        while start != iterable.index(stop):
            if i % abs(step) == 0:
                result.append(iterable[start])
            if step > 0:
                start += 1
            else:
                start -= 1
            i += 1
        return result
    result = []
    i = 0
    while iterable.index(start) != iterable.index(stop):
        if i % abs(step) == 0:
            result.append(iterable[iterable.index(start)])
        if step > 0:
            index = iterable.index(start)
            index += 1
            start = iterable[index]

        else:
            index = iterable.index(start)
            index -= 1
            start = iterable[index]

        i += 1
    return result