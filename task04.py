"""
Classic task, a kind of walnut for you

Given four lists A, B, C, D of integer values,
    compute how many tuples (i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] is zero.

We guarantee, that all A, B, C, D have same length of N where 0 ≤ N ≤ 1000.
"""
import collections
from typing import List


def check_sum_of_four(a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
    count = collections.Counter(a + b for a in A for b in B)  # The Counter() class allows you to count an immutable number of elements, in our case these elements are the sum of a + b.
    return sum(count[-c - d] for c in C for d in D)  # On the difference of c and d we pick up the key to the counter dictionary and summarize, if there is a match