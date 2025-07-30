import asyncio
import random
import string
import asyncio
import random
import threading
import sys


def random_print_str():
    """
    Prints a random string.
    :return:  None
    """
    str_len = random.randint(1, 20)
    print("".join(random.choices(string.ascii_letters + string.digits, k=str_len)))


def async_crash_with_random_time_in_1_minute():
    """
    Starts a background task that crashes the program after a random delay (1 to 60 seconds).
    Can be called from synchronous code.
    """
    def _crash_worker():
        async def _delayed_crash():
            delay = random.randint(1, 60)
            await asyncio.sleep(delay)
            raise RuntimeError("UselessLib: Crashed after random delay.")
        try:
            asyncio.run(_delayed_crash())
        except Exception as e:
            print(e)
            sys.exit(1)
    t = threading.Thread(target=_crash_worker, daemon=False)
    t.start()
