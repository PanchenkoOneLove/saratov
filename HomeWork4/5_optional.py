"""
This task is optional.

Write a generator that takes a number N as an input
and returns a generator that yields N FizzBuzz numbers*
Don't use any ifs, you can find an approach for the implementation in this video**.


Definition of done:
 - function is created
 - function is properly formatted
 - function has tests


>>> list(fizzbuzz(5))
["1", "2", "fizz", "4", "buzz"]

* https://en.wikipedia.org/wiki/Fizz_buzz
** https://www.youtube.com/watch?v=NSzsYWckGd4
"""
from typing import List, Generator


def fizzbuzz(n: int) -> Generator[str]:
    mappings = {3: 'fizz', 5: 'buzz'}
    for i in range(1, N + 1):
        result = ''.join(value for key, value in mappings.items() if i % key == 0)
        yield result or str(i)
