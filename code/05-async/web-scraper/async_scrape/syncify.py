import asyncio
import threading
import time
import uuid
from typing import Any, Coroutine

initialized = False

__add_lock = threading.Lock()
__receive_lock = threading.Lock()

pending_items: dict[uuid.uuid4, Coroutine[Any, Any, Any]] = {}
finished_items: dict[uuid.uuid4, Any] = {}


class ReentrancyException(Exception):
    pass


def run(async_coroutine: Coroutine[Any, Any, Any]):
    """
    Convert an async method to a synchronous one.

    Example:

        async def some_async_method(x, y): ...

        result = syncify.run( some_async_method(1, 2) )

    Args:
        async_coroutine ():

    Returns: The value returned by `async_coroutine`

    """

    item_id = __add_work(async_coroutine)
    while not __is_done(item_id):
        time.sleep(0.0005)
        continue

    result = __get_result(item_id)
    if isinstance(result, Exception):
        raise SyncifyRuntimeError() from result

    return result


class SyncifyRuntimeError(Exception):
    pass


def worker_loop():
    print(f"Starting syncify background thread.")
    loop = asyncio.new_event_loop()

    while True:
        with __add_lock:
            count = len(pending_items)

        if count == 0:
            time.sleep(0.001)
            continue

        try:

            with __add_lock:
                work: list[(uuid.uuid4, Coroutine[Any, Any, Any])] = list(pending_items.items())
                for k, w in work:
                    del pending_items[k]

            running: dict[uuid.uuid4, asyncio.Task] = {
                k: loop.create_task(w)
                for k, w in work
            }

            for k, t in running.items():
                try:
                    loop.run_until_complete(asyncio.wait([t]))
                    result = t.result()
                    with __receive_lock:
                        finished_items[k] = result
                except Exception as x:
                    with __receive_lock:
                        finished_items[k] = x

        except Exception as x:
            print("Error processing pending tasks:")
            print(x)


def __add_work(async_coroutine: Coroutine[Any, Any, Any]) -> uuid.uuid4:
    if threading.current_thread().native_id == worker_thread.native_id:
        msg = f'Cannot schedule coroutine {async_coroutine}, cannot schedule async -> sync work ' \
              f'from async execution. Await the async version of {async_coroutine} instead of syncifying it.'
        print(msg)
        raise ReentrancyException(msg)

    new_id = uuid.uuid4()

    with __add_lock:
        pending_items[new_id] = async_coroutine

    return new_id


def __is_done(item_id: uuid.uuid4) -> bool:
    with __receive_lock:
        return item_id in finished_items


def __get_result(item_id: uuid.uuid4) -> Any:
    with __receive_lock:
        result = finished_items[item_id]
        del finished_items[item_id]

    return result


worker_thread = threading.Thread(name="syncify-thread", target=worker_loop, daemon=True)
worker_thread.start()
