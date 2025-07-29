import asyncio
import time

from .asyncio import run_in_threadpool
from .utils import DummyStopIteration, next_without_stop_iteration


async def to_aiterator(iterator):
    iterator = await run_in_threadpool(iter, iterator)
    while True:
        try:
            yield await run_in_threadpool(next_without_stop_iteration, iterator)
        except DummyStopIteration:
            break


async def rate_limit_iterator(aiterator, iters_per_second):
    start = time.time()
    i = 0
    async for it in aiterator:
        yield it
        await asyncio.sleep((i / iters_per_second) - (time.time() - start))
        i += 1
