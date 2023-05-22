from typing import Callable


def cache(times: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        cached_results = {}  # Dictionary to store cached results
        remaining_times = times  # Number of remaining attempts to use the cached value

        def cached_func(*args, **kwargs):
            nonlocal remaining_times  # Declare remaining_times as a variable accessible for modification within the closure
            key = args + tuple(kwargs.items())  # Form the key based on the function arguments
            if key in cached_results:  # If the result is already cached for this key
                remaining_times -= 1  # Decrease the number of remaining attempts to use the cached value
                if remaining_times >= 0:  # If there are non-negative attempts remaining, return the cached value
                    return cached_results[key]
            result = func(*args, **kwargs)  # Call the original function to get a new value
            cached_results[key] = result  # Cache the new value
            remaining_times = times - 1  # Update the number of remaining attempts, resetting the counter after returning a new value
            return result

        return cached_func  # Return the wrapper function

    return decorator  # Return the decorator