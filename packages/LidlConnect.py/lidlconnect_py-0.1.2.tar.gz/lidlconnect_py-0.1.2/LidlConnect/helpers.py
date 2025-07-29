"""Helper functions for Lidl Connect library."""

from functools import wraps
import time

def ttl_cache(ttl_seconds=30):
    """
    Time-based cache decorator.
    
    Args:
        ttl_seconds: Number of seconds to cache the result
        
    Returns:
        Decorated function with caching
    """
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = str(args) + str(kwargs)
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache = cache
        return wrapper
    return decorator