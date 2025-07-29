# ──────────────────────────────────────────────────────────────────────────────────────
#                               TRACELINE ASYNC LOGGER
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : AsyncLogger.py
#     Module Name    : Traceline Async Logger
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.4
#
# FILE DESCRIPTION:
#     Provides a robust, thread-safe asynchronous logging engine using
#     Python's threading.Queue and background worker pattern. Designed
#     for high-throughput, low-latency structured logging environments.
#
# PROGRAM DESCRIPTION:
#     Primary Features:
#         - Thread-safe log queue with overflow protection
#         - Background worker thread with graceful shutdown
#         - pluggable formatter and log backend
#         - Rust-style Result error handling
#         - fault isolation to prevent logger failures from affecting application
#
# SECURITY CONSIDERATIONS:
#     - Handles all I/O with retry-safe logic
#     - Path is restricted to local `.log/` folder
#     - Message sanitization prevents injection
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : threading, queue, sys, dataclasses, typing, returns
#
# USAGE:
#     >>> from traceline import AsyncLogger, LogType
#     >>> logger = AsyncLogger(name="MyApp", max_queue_size=5000)
#     >>> logger.start()
#     >>> logger.log("Application started", LogType.INFO)
#     >>> logger.log("Debug information", LogType.DEBUG)
#     >>> logger.stop(timeout=5.0)
#     >>>
#     >>> # With custom output function
#     >>> def custom_output(msg: str, logtype: LogType) -> Result[str, Exception]:
#     ...     return Success(f"CUSTOM: {msg}")
#     >>> async_logger = AsyncLogger(output_fn=custom_output)
#     >>> async_logger.start()
#
# SYSTEM INTEGRATION:
#     Part of        : HYRA‑0 – Zero‑Database Mathematical & Physical Reasoning Engine
#     Subsystem      : Traceline Logging Core
#
# MAINTAINABILITY:
#     Author         : Michael Tang
#     Organization   : BioNautica Research Initiative
#     Contact        : michaeltang@bionautica.org
#     Created        : 2025‑07‑01
#     Last Updated   : 2025‑07‑11
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import threading
import queue
import sys
import time

from dataclasses import dataclass
from typing import Callable
from returns.result import Result, Success, Failure
from enum import Enum, auto

from .Types import LogType, Color, get_color
from .Log import log

# Constants
MAX_RETRY_BACKOFF = 5.0  # Maximum retry timeout for queue operations
_SHUTDOWN_SENTINEL: object = object()  # Sentinel value to signal shutdown

# Task Model
@dataclass(frozen=True)
class LogTask:
    message: str
    logtype: LogType

# State
class WorkerState(Enum):
    STOPPED     = auto()
    RUNNING     = auto()
    STOPPING    = auto()

# AsyncLogger Main Class
class AsyncLogger:
    """
    Asynchronous thread-based logger using producer-consumer pattern.
    """

    def __init__(
            self,
            name: str = "Traceline AsyncLogger",
            loglevel: LogType = LogType.INFO,
            flush_interval: float = 0.5,
            max_queue_size: int = 10000,
            output_fn: Callable[[str, LogType], Result[str, Exception]] = log
    ) -> None:
        """
        Initialize AsyncLogger with configuration
        """
        self._name = name.strip()
        self._loglevel = loglevel
        self._flush_interval = flush_interval
        self._output_fn = output_fn

        from typing import Any
        self._queue: queue.Queue[Any] = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._worker_thread: threading.Thread | None = None
        self._started = False

        self._dropped_count = 0
        self._drop_lock = threading.Lock()

        self._state_lock = threading.Lock()
        self._state_condition = threading.Condition(self._state_lock)
        self._state: WorkerState = WorkerState.STOPPED

        self._restart_backoff = 0.5
        self._restart_backoff_max = 30.0

        # => Supervisor thread started to monitor and manage the worker thread
        self._supervisor_thread = threading.Thread(
            target=self._supervisor_loop,
            name=f"{self._name} Supervisor",
            daemon=True
        )
        self._supervisor_thread.start()

    def start(self) -> Result[bool, Exception]:
        """
        Thread-safe, idempotent start. Returns Success(True) if the
        logger is running (whether newly started or already running).
        """
        with self._state_lock:
            if self._state is WorkerState.RUNNING: # Already running
                return Success(True)
            if self._state is WorkerState.STOPPING: # Is stopping, wait for it to finish
                self._state_condition.wait_for(lambda: self._state is WorkerState.STOPPED)
            
            self._stop_event.clear()  # Reset stop event
            self._queue = queue.Queue(maxsize=self._queue.maxsize)
            self._worker_thread = threading.Thread(
                target=self._worker_loop,
                name=f"{self._name}",
                daemon=True
            )
            try:
                self._worker_thread.start()
                self._state = WorkerState.RUNNING
                self._restart_backoff = 0.5
                self._state_condition.notify_all()
                self._started = True
            except Exception as e:
                self._state = WorkerState.STOPPED
                self._state_condition.notify_all()
                return Failure(e)

        return self.log(f"{self._name} initialized.", LogType.DEBUG).map(lambda _: True)

    def stop(self, timeout: float = 2.0) -> Result[bool, Exception]:
        """
        Gracefully stop the worker. Safe to call multiple times.
        """
        with self._state_lock:
            if self._state is WorkerState.STOPPED:
                return Success(True)
            
            self._state = WorkerState.STOPPING
            self._stop_event.set()  # Notify the worker to stop
            self._state_condition.notify_all()
            worker = self._worker_thread # Keep a reference to the worker thread

        try:
            self._queue.put_nowait(_SHUTDOWN_SENTINEL)  # Immediately signal shutdown
        except queue.Full:
            # If the queue is full, we can still proceed to stop the worker
            pass

        self._queue.join()  # Wait for all tasks to be processed

        if worker and worker.is_alive():
            worker.join(timeout)
        
        with self._state_lock:
            self._state = WorkerState.STOPPED
            self._state_condition.notify_all()
            self._started = False
        
        return Success(True)
    
    def log(self, message: str, logtype: LogType = LogType.INFO) -> Result[bool, Exception]:
        """
        Queue a log message for asynchronous processing.
        """
        if not message.strip():
            return Failure(ValueError("Log message cannot be empty"))
        
        if logtype.value < self._loglevel.value:
            return Success(False)
        
        try:
            self._queue.put_nowait(LogTask(message, logtype))
            return Success(True)
        except queue.Full:
            with self._drop_lock:
                self._dropped_count += 1

            fallback = f"[{LogType.ERROR}] Log queue full. Dropped message: {message[:100]}"
            print(fallback, file=sys.stderr)
            return Failure(RuntimeError("Log queue overflow"))
        
    def print(self, message: str, logtype: LogType = LogType.INFO) -> Result[bool, Exception]:
        """
        Print log message to stdout/stderr immediately.
        """
        if not message.strip():
            return Failure(ValueError("Print message cannot be empty"))
        if logtype.value < self._loglevel.value:
            return Success(False)
        
        try:
            color_code = get_color(logtype)
            if isinstance(color_code, Failure):
                return Failure(color_code.failure())
            
            formatted = f"{color_code.unwrap().value}[{logtype.name}] " \
                        f"{Color.RESET.value}{message.strip()}"
            print(formatted, flush=True)
        except Exception as e:
            self._stderr_fallback(f"Print failed: {e}", logtype)

        return self.log(message, logtype).map(lambda _: True)
        
    def dropped_count(self) -> Result[int, Exception]:
        """
        Get the number of dropped log messages due to queue overflow.
        """
        with self._drop_lock:
            return Success(self._dropped_count)
        
    def reset_metrics(self) -> Result[bool, Exception]:
        """
        Reset dropped message count.
        """
        with self._drop_lock:
            self._dropped_count = 0
        return Success(True)
    
    @property
    def is_running(self) -> bool:
        with self._state_lock:
            return self._started and self._worker_thread is not None and self._worker_thread.is_alive()
    
# -------------------------------------------------------------------------------------------------------------------------------
# Private Methods

    def _worker_loop(self) -> None:
        """
        Background thread loop: drain the queue until stop event is set
        and the queue is empty.
        """
        try:
            while True:
                try:
                    task = self._queue.get(timeout=self._flush_interval)
                    if task is _SHUTDOWN_SENTINEL:
                        self._queue.task_done()
                        break
                    self._process(task)
                    self._queue.task_done()
                except queue.Empty:
                    if self._stop_event.is_set():
                        break
                    continue
        except Exception as e:
            self._stderr_fallback(f"Worker crashed: {e}", LogType.CRITICAL)
        finally:
            with self._state_lock:
                self._state = WorkerState.STOPPED
                self._state_condition.notify_all()

    def _process(self, task: LogTask) -> None:
        """
        Write single log message: any sink failure will be treated as a critical error.
        Hand off and pass to _worker_loop for processing, trigger supervisor to restart.
        """
        result = self._output_fn(task.message, task.logtype)
        if isinstance(result, Failure):
            raise result.failure()

    def _stderr_fallback(self, message: str, logtype: LogType) -> None:
        """
        Write to stderr in case of logging failure.
        """
        print(f"[{logtype.name}] {message}", file=sys.stderr, flush=True)

    def _supervisor_loop(self) -> None:
        while True:
            with self._state_lock:
                self._state_condition.wait_for(lambda: self._state is WorkerState.STOPPED)
                old_worker = self._worker_thread
                should_restart = not self._stop_event.is_set()

            if old_worker is not None:
                old_worker.join()

            if should_restart:
                time.sleep(self._restart_backoff)
                self._restart_backoff = min(self._restart_backoff * 2, self._restart_backoff_max)
                self.start()
            else:
                with self._state_lock:
                    self._restart_backoff = 0.5
                time.sleep(0.5)  # Avoid busy-waiting

# ========================================================= END OF FILE =========================================================
