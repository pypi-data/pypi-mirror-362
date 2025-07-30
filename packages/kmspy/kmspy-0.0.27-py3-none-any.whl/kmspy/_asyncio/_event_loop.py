import asyncio
from functools import partial
from typing import Awaitable

import asyncio
import threading
from typing import Awaitable, Any, Callable, Optional


class SafeEventLoop:
    """function, coro, future를 안전하게 실행할 수 있는 루프 클래스"""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self._loop = loop or asyncio.new_event_loop()
        self._is_running = False
        self._thread = threading.Thread(target=self._start_loop, daemon=True)
        self._thread.start()

    def _start_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def create_task(self, coro_or_future: Callable, *args, **kwargs) -> Awaitable[Any]:        
        return self._loop.run_in_executor(None, partial(self.run, coro_or_future, **kwargs), *args)

    def run_in_executor(self, executor, fn, *args):
        return self._loop.run_in_executor(executor, fn, *args)

    def run(self, coro: Awaitable[Any]) -> Any:
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def call_soon(self, fn: Callable, *args, **kwargs):
        self._loop.call_soon_threadsafe(fn, *args, **kwargs)

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()