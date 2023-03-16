"""
Write a function that accepts another function as an argument. Then it
should return such a function, so the every call to initial one
should be cached.


def func(a, b):
    return (a ** b) ** 2


cache_func = cache(func)

some = 100, 200

val_1 = cache_func(*some)
val_2 = cache_func(*some)

assert val_1 is val_2

"""
import collections
from collections.abc import Callable

'''
This code uses the cache() function to cache the results of func().
The func() function simply returns the arithmetic mean of the two numbers a and b. 
The cache() function creates an empty dictionary in the cached_results variable, then it calls itself, 
using that dictionary to cache the results of func().
On each call, the cache() function first compares arguments to key-value pairs from the cached_results dictionary. 
If the key exists, it returns the corresponding value from the dictionary. 
If the key does not exist in the dictionary,
the result returned by func() will be added to the dictionary under the corresponding key. 
At the end of each call to cache() will return the result, which was stored in the dictionary. 
'''


def func(a, b):
    return (a + b) / 2


def cache(func: Callable) -> Callable:
    cached_results = {}

    def cached_func(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key in cached_results:
            return cached_results[key]
        result = func(*args, **kwargs)
        cached_results[key] = result
        return cached_results

    return cached_func



