"""
Write down the function, which reads input line-by-line, and find maximum and minimum values.
Function should return a tuple with the max and min values.
For example for [1, 2, 3, 4, 5], function should return [1, 5]
We guarantee, that file exists and contains line-delimited integers.
To read file line-by-line you can use this snippet:
with open("some_file.txt") as fi:
    for line in fi:
        ...
"""
from typing import Tuple


def find_maximum_and_minimum(file_name: str) -> Tuple[int, int]:
    with open(file_name, "r") as fi:
        data = []
        for line in fi:
            data.append([int(x) for x in line.split()]) # Adding the value read from each line of the file to an empty array
        min_value = data[0]
        max_value = data[0]
        for i in range(len(data)):  # We calculate the minimum and maximum values
            if min_value > data[i]:
                min_value = data[i]
            if max_value < data[i]:
                max_value = data[i]
        x = tuple(max_value, min_value)
        return x