import asyncio
import random
from functools import wraps

def async_backoff(
    retries=5,
    base_delay=1,
    max_delay=60,
    jitter=True,
    exceptions=(Exception,)
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == retries - 1:
                        raise
                    sleep_time = delay + random.uniform(0, delay) if jitter else delay
                    sleep_time = min(sleep_time, max_delay)
                    print("-----------------------------------------------------------")
                    print(f"[Retry {attempt + 1}] {e} — sleeping for {sleep_time:.2f} seconds...")
                    await asyncio.sleep(sleep_time)
                    delay *= 2
        return wrapper
    return decorator
