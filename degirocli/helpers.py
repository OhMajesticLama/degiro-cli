import enum
import logging
import asyncio
import collections
from typing import Callable
from typing import Iterable
from typing import Any
from typing import Sequence
from typing import Union


LOGGER = logging.getLogger('degirocli')

class ERROR_CODES(enum.IntEnum):
    SESSION_EXISTS = 1

async def run_concurrent(
        worker: Callable,
        jobs: Iterable[Any],
        *,
        max_concurrents: int = 10,
        ) -> Sequence[collections.abc.Awaitable]:
    """
    Run worker on jobs with a max of max_concurrents at the same time.

    This is a helper to avoid sending too many queries at once to the producer
    queried by worker.

    >>> import asyncio
    >>> async def worker(a, b):
    ...     await asyncio.sleep(1)
    ...     return a + b
    ...
    >>> awaitables = await run_concurrent(worker,
    ...                             ((1, 2), (2, 3)))
    ...
    >>> res1 = await awaitables[0]
    >>> res1
    3

    Arguments
    ---------
    
    worker
        Callable to apply to jobs.

    jobs
        Iterable of arguments that will be passed to worker.

    max_concurrents
        Maximum number of jobs that will be run concurrently.
    """
    LOGGER.debug('run_concurrent| worker %s', worker)
    work_sem = asyncio.Semaphore(max_concurrents)

    async def _wrapper(attrs):
        async with work_sem:
            res = await worker(*attrs)
        return res

    return [asyncio.create_task(_wrapper(attrs)) for attrs in jobs]
