import time
import struct
import random
import hashlib
from multiprocessing import Pool


def slow_calculate(value):
    """Some weird voodoo magic calculations"""
    time.sleep(random.randint(1, 3))
    data = hashlib.md5(str(value).encode()).digest()
    return sum(struct.unpack('<' + 'B' * len(data), data))


def calculate_total_sum():
    with Pool() as pool:
        numbers = range(501)  # Generate numbers from 0 to 500
        results = pool.map(slow_calculate, numbers)  # Process numbers in parallel
        total_sum = sum(results)  # Calculate the total sum of the results
    return total_sum
