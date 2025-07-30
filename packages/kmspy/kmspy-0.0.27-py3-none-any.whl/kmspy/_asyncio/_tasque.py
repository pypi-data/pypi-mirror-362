import asyncio
import concurrent
from functools import partial, wraps
from threading import Thread
from typing import Any, Callable, List, Optional
from uuid import uuid4

from ._event_loop import SafeEventLoop


class CancelledError(Exception):
    pass


class TaskFuture:
    def __init__(self,
                 coro_or_callable,
                 *args,
                 loop: SafeEventLoop = None,
                 start=False,
                 **kwargs):
        self._safe_event_loop = loop or SafeEventLoop()
        self._cancel_requested = False
        self._done_event = asyncio.Event()
        self._result = None
        self._exception = None
        self._task = None
        self._coro_or_future = self._runner(coro_or_callable, *args, **kwargs)
        self._started = False
        if start:
            self.start()
    
    def check_started(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            self.start()
            return fn(self, *args, **kwargs)
        return wrapper

    def start(self):
        """지연 실행을 위한 메소드
        
        TaskFuture 객체를 생성할 때 start=True라면 task로 생성하여 바로 함수를 실행한다.
        start=False로 만들었다면 result() 호출 또는 await를 사용하면 그때 task를 만든다."""
        if self._started:
            return
        self._started = True
        self._task = self._safe_event_loop.create_task(self._coro_or_future)

    async def _runner(self, fn, *args, **kwargs):
        """동기함수, 비동기함수를 입력 받아서 await가 가능한 객체를 만든다.

        동기함수는 run_in_executor로 Future를 생성하고,
        비동기함수는 coroutine을 반환한다.
        """
        if asyncio.iscoroutinefunction(fn):
            coro_or_future: asyncio.Future = self._safe_event_loop.create_task(fn(*args, **kwargs))
        else:
            if kwargs:
                fn = partial(fn, **kwargs)
            coro_or_future: asyncio.Future = self._safe_event_loop.run_in_executor(None, fn, *args)
        try:
            if self._cancel_requested:
                raise CancelledError()
            self._result = await coro_or_future
            if asyncio.iscoroutine(self._result):
                self._result = await self._result
            if self._cancel_requested:
                raise CancelledError()
        except Exception as e:
            self._exception = e
        finally:
            self._done_event.set()    

    def cancel(self):
        if self.done():
            return False
        self._cancel_requested = True
        if self._task and not self._task.done():
            self._task.cancel()
        return True

    def cancelled(self):
        return self._cancel_requested or (self._exception is not None and isinstance(self._exception, CancelledError))

    def done(self):
        """끝났는지 확인하는 메소드"""
        return self._done_event.is_set()

    @check_started
    def as_future(self):
        async def _await_task(task):
            return await task
        return asyncio.run_coroutine_threadsafe(_await_task(self._task), self._safe_event_loop._loop)
    
    @check_started
    def result(self, timeout: Optional[float] = None) -> Any:
        """동기로 결과 받아오는 함수"""
        if not self.done():
            self._safe_event_loop.run(self._done_event.wait())
        if self._exception:
            raise self._exception
        return self._result

    @check_started
    async def _await_result(self):
        """비동기로 결과 받아오는 함수

        직접 호출하지 않고 아래의 __await__ 메소드를 사용하는 await future로 사용 권장"""
        await self._done_event.wait()
        if self._exception:
            raise self._exception
        return self._result

    @check_started
    def __await__(self):
        """TaskFuture 객체를 await 가 가능하게 만든다.
        
        task = TaskFuture(coro_or_callable)
        result = await task
        """
        return self._await_result().__await__()


class TaskQueue:
    def __init__(self, max_concurrency: int = 5, loop: Optional[SafeEventLoop] = None):
        self._max_concurrency = max_concurrency
        self._safe_event_loop = loop or SafeEventLoop()
        self._queue = asyncio.Queue()
        self._worker_done = asyncio.Queue()
        self._worker_queue = asyncio.Queue(maxsize=max_concurrency)
        self._active = 0
        self._lock = asyncio.Lock()
        self._stopped = False
        self._workers = {}
        self._generate_worker_thread = Thread(target=self._generate_worker)
        self._init_worker()

    def _init_worker(self):
        for _ in range(self._max_concurrency):
            self._worker_queue.put_nowait(str(uuid4()))

    def _generate_worker(self):     
        while True:
            try:
                uuid = self._safe_event_loop.run(self._worker_done.get())
                self._workers.pop(uuid)
                self._worker_done.task_done()
                w = self._safe_event_loop.create_task(self._worker(self._safe_event_loop.run(self._queue.get()), uuid))
                self._workers[uuid] = w
            except Exception as e:
                pass
        

    async def _worker(self, fn_future: TaskFuture, uuid: str):
        """워커를 만든다.

        워커는 self._queue에서 TaskFuture를 하나 꺼내서 결과를 받는다.
        여기서 받는 결과는 실제 값이 아니라 결과가 나왔는지 여부라고 볼 수 있다.
        """
        async with self._lock:
            self._active += 1
        try:
            if fn_future.cancelled():
                pass
            else:
                await fn_future
        except Exception:
            pass
        finally:
            async with self._lock:
                self._active -= 1
            self._queue.task_done()
            self._worker_done.put_nowait(uuid)

    def create_task(self, fn: Callable, *args, **kwargs) -> TaskFuture:
        tf = TaskFuture(fn, loop=self._safe_event_loop, start=True, *args, **kwargs)
        self._queue.put_nowait(tf)
        return tf

    def submit(self, fn: Callable, *args, **kwargs) -> TaskFuture:
        tf = TaskFuture(fn, loop=self._safe_event_loop, start=False, *args, **kwargs)
        self._queue.put_nowait(tf)
        return tf
            
    async def join(self):
        await self._queue.join()

    def stop(self):
        self._stopped = True
        for w in self._workers:
            w.cancel()
        self._safe_event_loop.stop()
        

    def as_completed(self, tasks: List[TaskFuture]):
        # asyncio.as_completed의 결과로 나오는 coroutine과 TaskFuture 사이의 관계가 있을까??
        # 만약 있다면, as_completed가 메소드 종료 여부만 알려주는 것이고, 매칭되는 TaskFuture의 결과를 yield로 내보내거나, TaskFuture 자체를 yield로 뱉으면 될듯
        pass

    def gather(self, tasks: List[TaskFuture]):
        # 이건 gather를 할 필요도 없고 tasks를 list comprehension으로 result 바로 뱉으면 됨
        pass


_default_queue: Optional[TaskQueue] = None
_default_loop: Optional[SafeEventLoop] = None


def _get_default_queue() -> TaskQueue:
    global _default_queue, _default_loop
    if _default_queue is None:
        _default_loop = SafeEventLoop()
        _default_queue = TaskQueue(max_concurrency=5, loop=_default_loop)
    return _default_queue


def set_config(max_concurrency: int = 5, loop: asyncio.AbstractEventLoop = None):
    global _default_queue, _default_loop
    if _default_loop:
        _default_loop.stop()
    _default_loop = SafeEventLoop(loop)
    _default_queue = TaskQueue(max_concurrency=max_concurrency, loop=_default_loop)


def create_task(fn: Callable, *args, **kwargs) -> TaskFuture:
    queue = _get_default_queue()
    return queue.create_task(fn, *args, **kwargs)


def submit(fn: Callable, *args, **kwargs) -> TaskFuture:
    queue = _get_default_queue()
    return queue.submit(fn, *args, **kwargs)


def run(fn: Callable, *args, **kwargs) -> Any:
    queue = _get_default_queue()
    tf = queue.create_task(fn, *args, **kwargs)
    return tf.result()


def as_completed(task_futures: List[TaskFuture]):
    # asyncio.Task만 뽑아서 run_coroutine_threadsafe로 Future 만들기
    cfut_to_tf = {tf.as_future(): tf for tf in task_futures}

    for cfut in concurrent.futures.as_completed(cfut_to_tf):
        tf = cfut_to_tf[cfut]
        try:
            yield tf.result()  # 또는 tf.result() if wrapping logic is needed
        except Exception as e:
            yield e


def gather(task_futures: List[TaskFuture]) -> List[Any]:
    [tf.start() for tf in task_futures]
    return [tf.result() for tf in task_futures]


def stop():
    _default_queue.stop()