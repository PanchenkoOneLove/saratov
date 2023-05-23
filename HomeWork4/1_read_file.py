"""
Write a function that gets file path as an argument.
Read the first line of the file.
If first line is a number return true if number in an interval [1, 3)*
and false otherwise.
In case of any error, a ValueError should be thrown.

Write a test for that function using pytest library.

Definition of done:
 - function is created
 - function is properly formatted
 - function has positive and negative tests
 - all temporary files are removed after test run

You will learn:
 - how to test Exceptional cases
 - how to clean up after tests
 - how to check if file exists**
 - how to handle*** and raise**** exceptions in test. Use sample from the documentation.

* https://en.wikipedia.org/wiki/Interval_(mathematics)#Terminology
** https://docs.python.org/3/library/os.path.html
*** https://docs.python.org/3/tutorial/errors.html#handling-exceptions
**** https://docs.python.org/3/tutorial/errors.html#raising-exceptions
"""


import numpy as np


def read_magic_number(path: str) -> bool:
    try:
        with open(path, 'r') as file:
            first_line = file.readline().strip()
            try:
                number = float(first_line)
                return 1 <= number < 3
            except ValueError:
                return False
    except FileNotFoundError:
        raise ValueError("File not found.")
    except IOError:
        raise ValueError("Error reading file.")
