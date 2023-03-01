"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List



def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    subsum = 0
    elements_sum = []
    for i in range(len(nums)):
        for j in range(k):
            if j > i:
                break
            else:
                for g in range(j+1):
                    subsum += nums[i-g]
                if len(elements_sum) < i+1:
                    elements_sum.append(subsum)
                elif subsum > elements_sum[i]:
                    elements_sum[i] = subsum
                subsum = 0
    return max(elements_sum)  # Among all possible sums, we choose the maximum one using the max function


