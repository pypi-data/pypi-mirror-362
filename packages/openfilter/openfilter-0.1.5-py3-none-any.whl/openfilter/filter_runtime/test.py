"""Misc stuff for testing."""

import logging
import multiprocessing as mp
from collections.abc import Mapping, Sequence
from multiprocessing.queues import Queue as mp_Queue, Empty as mp_Empty, Full as mp_Full
from queue import Queue, Full
from threading import Event, Thread
from time import sleep
from threading import RLock
from types import ModuleType
from typing import Any

from .filter import Filter, FilterConfig, POLL_TIMEOUT_SEC

__all__ = ['almost_equal', 'Docker', 'docker', 'ContainerContext', 'RunnerContext',
    'FiltersQueueConfig', 'QueueToFilters', 'FiltersToQueue']

logger = logging.getLogger(__name__)


def almost_equal(a: Any, b, delta: float = 0.000001):
    """Deep compare of two data structures comparing numeric types fuzzily. All other structure must match and be equal."""

    if isinstance(a, (int, float)):
        if not isinstance(b, (int, float)):
            return False

        return abs(a - b) <= delta

    if isinstance(a, Mapping):
        if not isinstance(b, Mapping) or set(keys := a.keys()) != set(b.keys()):
            return False

        if any(not almost_equal(a[k], b[k], delta) for k in keys):
            return False

        return True

    if not isinstance(a, str) and isinstance(a, Sequence):
        if not isinstance(b, Sequence) or len(a) != len(b):
            return False

        if any(not almost_equal(a[i], b[i], delta) for i in range(len(a))):
            return False

        return True

    try:
        return a == b
    except Exception:
        return False


class Docker:
    """Lazy import of docker module and client get."""

    lock = RLock()

    @property
    def module(self) -> ModuleType:
        try:
            return self._module
        except AttributeError:
            pass

        with self.lock:
            try:
                return self._module
            except AttributeError:
                pass

            import docker as module  # 'docker-py' package

            self._module = module

            return module

    @property
    def client(self):  # -> 'docker.client.DockerClient':
        try:
            return self._client
        except AttributeError:
            pass

        with self.lock:
            try:
                return self._client
            except AttributeError:
                pass

            self._client = client = self.module.from_env()

            return client

docker = Docker()


class ContainerContext:
    environment = {}
    image       = None
    kwargs      = {}

    def __init__(self, environment={}, image=None, logs=True, **kwargs):
        self.environment = {**self.environment, **environment}
        self.image       = self.image if image is None else image
        self.kwargs      = {**self.kwargs, **kwargs}
        self.logs        = logs

    def __enter__(self):
        self.container = docker.client.containers.run(self.image, environment=self.environment, **self.kwargs)

        return self.container

    def __exit__(self, exc_type, exc_value, traceback):
        auto_remove = self.kwargs.get('remove') or self.kwargs.get('auto_remove')

        try:
            self.container.stop()

        except Exception as exc:
            if auto_remove and isinstance(exc, docker.module.errors.NotFound):  # if container is autoremove and is not there then its not a surprise
                return

            logger.error(exc)

        if self.logs:
            try:
                logs = self.container.logs().decode('utf-8')

                (logger.critical if ' CRITICAL ' in logs else logger.error if ' ERROR ' in logs else
                    logger.warning if ' WARNING ' in logs else logger.info)('--- LOGS FROM CONTAINER ---\n\n' + logs)

            except Exception as exc:
                if auto_remove and isinstance(exc, docker.module.errors.NotFound):  # its like a ninja, it can disappear at any moment
                    return

                if not auto_remove or not isinstance(exc, docker.module.errors.APIError):
                    logger.error(exc)

        try:
            self.container.remove()

        except Exception as exc:
            if auto_remove and isinstance(exc, docker.module.errors.NotFound):  # *POOF*
                return

            logger.error(exc)


class RunnerContext:
    def __init__(self, filters, finalizers, **kwargs):
        self.filters    = filters
        self.finalizers = finalizers
        self.kwargs     = kwargs

    def __enter__(self):
        self.runner = Filter.Runner(self.filters, **self.kwargs)

        return self.runner

    def __exit__(self, exc_type, exc_value, traceback):
        self.runner.stop()

        for finalizer in self.finalizers:
            if isinstance(finalizer, (mp_Queue, FiltersToQueue.Queue)):
                finalizer.close()
            else:
                finalizer()


class FiltersQueueConfig(FilterConfig):
    queue: mp_Queue


class QueueToFilters(Filter):
    """Put False into the queue to initiate a clean exit or a BaseException to raise that. Put int or float to sleep."""

    def process(self, frames):
        while True:
            try:
                frames = self.config.queue.get(timeout=POLL_TIMEOUT_SEC)
            except mp_Empty:
                return None

            if frames is False:
                self.exit()
            elif isinstance(frames, BaseException):
                raise frames
            elif not isinstance(frames, (int, float)):
                break

            sleep(frames)

        return frames


class FiltersToQueue(Filter):
    """Puts False into the queue upon exit."""

    def process(self, frames):
        try:
            self.config.queue.put(frames, timeout=POLL_TIMEOUT_SEC)
        except mp_Full:
            pass

    def shutdown(self):
        try:
            self.config.queue.put(False, block=False)  # put done marker
        except mp_Full:
            pass

    class Queue(Queue):
        """Non-intrusive way of handling multiprocessing Queue cleanly (due to potential hang in .join() if not all data
        from queue has been consumed). Constantly reads from multiprocessing queue to ensure it is empty and the process
        is join()able. Meant for child process sending data to parent, won't work the other way."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.child_queue = mp.Queue()
            self.stop_evt    = Event()
            self.thread      = Thread(target=self.thread_func, args=(self.child_queue, self.stop_evt), daemon=True)

            self.thread.start()

        def close(self):
            self.stop_evt.set()
            self.thread.join()
            self.child_queue.close()
            self.child_queue.join_thread()

        def thread_func(self, child_queue, stop_evt):
            while not stop_evt.is_set():
                try:
                    data = child_queue.get(timeout=POLL_TIMEOUT_SEC)
                except mp_Empty:
                    continue

                try:
                    self.put(data)
                except Full:
                    pass

                if data is False:
                    break
