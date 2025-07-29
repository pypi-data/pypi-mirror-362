# ──────────────────────────────────────────────────────────────────────────────────────
#                             TRACELINE ASYNC LOGGER TESTS
#                              (Comprehensive Unit Tests)
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : test_AsyncLogger.py
#     Module Name    : Traceline Async Logger Tests
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.4
#
# SYSTEM INTEGRATION:
#     Part of        : HYRA‑0 – Zero‑Database Mathematical & Physical Reasoning Engine
#     Subsystem      : Traceline Logging Core
#
# MAINTAINABILITY:
#     Author         : Michael Tang
#     Organization   : BioNautica Research Initiative
#     Contact        : michaeltang@bionautica.org
#     Created        : 2025‑07‑07
#     Last Updated   : 2025‑07‑11
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import threading
import time
import pytest
import queue
import builtins

from returns.result import Success, Failure, Result
from typing import Callable, TypedDict, Tuple, Any

from Traceline.AsyncLogger import AsyncLogger, WorkerState
from Traceline.Types import LogType

# Type Aliases ------------------------------------------------------------------------------------------------------------------

OutputFn = Callable[[str, LogType], Result[str, Exception]]

class HitsDict(TypedDict):
    """
    Shared counter for the fake sink.
    """
    count: int
    fail_next: bool

# Fixtures and Mocks ------------------------------------------------------------------------------------------------------------

@pytest.fixture
def sink_counter() -> Tuple[OutputFn, HitsDict]:
    """
    Produce (output_fn, hits).
    output_fn increments hits["count"] can be forced to fail once.
    """
    hits: HitsDict = {"count": 0, "fail_next": False}

    def _output_fn(message: str, logtype: LogType) -> Result[str, Exception]:
        hits["count"] += 1
        if hits["fail_next"]:
            hits["fail_next"] = False
            return Failure(RuntimeError("Forced sink failure"))
        return Success("OK")
    
    return _output_fn, hits

# Lifecycle ---------------------------------------------------------------------------------------------------------------------

def test_start_stop_idempotent(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn)

    # Multiple idempotent starts and stops
    assert logger.start().unwrap() is True
    assert logger.start().unwrap() is True
    assert logger.is_running
    assert logger.stop().unwrap() is True
    assert logger.stop().unwrap() is True

def test_worker_state_transitions(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn)

    assert logger._state is WorkerState.STOPPED  # pyright: ignore[reportPrivateUsage]
    logger.start().unwrap()
    assert logger._state is WorkerState.RUNNING  # pyright: ignore[reportPrivateUsage]
    logger.stop().unwrap()
    assert logger._state is WorkerState.STOPPED  # pyright: ignore[reportPrivateUsage]

def test_stop_waits_for_drain(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(output_fn=fn)

    logger.start().unwrap()
    for _ in range(5):
        assert logger.log("Message").unwrap() # Enqueue

    assert hits["count"] < 5
    assert logger.stop().unwrap() is True
    assert hits["count"] == 5 # Drained

# Validation / Guard-rail -------------------------------------------------------------------------------------------------------

def test_reject_empty_message(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn)
    logger.start().unwrap()
    
    result = logger.log("   \t\n  ")  # Empty message should return Failure
    assert isinstance(result, Failure)
    assert isinstance(result.failure(), ValueError)
    logger.stop().unwrap()

def test_log_level_threshold(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(loglevel=LogType.ERROR, output_fn=fn)

    logger.start().unwrap()
    assert logger.log("Debug message", logtype=LogType.DEBUG).unwrap() is False  # Below threshold
    assert logger.log("Info message", logtype=LogType.INFO).unwrap() is False  # Below threshold
    assert logger.log("Warning message", logtype=LogType.WARNING).unwrap() is False  # Below threshold
    assert logger.log("Error message", logtype=LogType.ERROR).unwrap() is True  # At threshold
    assert logger.log("Critical message", logtype=LogType.CRITICAL).unwrap() is True  # Above threshold
    logger.stop().unwrap()

    assert hits["count"] == 2  # Only ERROR and CRITICAL logged

def test_print_immediate_stdout_and_async_write(sink_counter: Tuple[OutputFn, HitsDict],
                                                capsys: pytest.CaptureFixture[str]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(output_fn=fn)
    logger.start().unwrap()

    assert logger.print("Hello from print()", LogType.INFO).unwrap() is True  # Should print immediately
    logger.stop().unwrap()

    captured = capsys.readouterr()
    assert "[INFO]" in captured.out
    assert hits["count"] == 1

def test_print_respects_loglevel_threshold(capsys: pytest.CaptureFixture[str]) -> None:
    fake_sink: OutputFn = lambda msg, lvl: Success("OK")
    logger = AsyncLogger(loglevel=LogType.ERROR, output_fn=fake_sink)
    logger.start().unwrap()

    assert logger.print("Invisible message", LogType.DEBUG).unwrap() is False  # Below threshold
    logger.stop().unwrap()

    captured = capsys.readouterr()
    assert captured.out == ""

def test_print_rejects_empty_message(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn)
    logger.start().unwrap()

    result = logger.print("         ", LogType.INFO)
    assert isinstance(result, Failure) and isinstance(result.failure(), ValueError)

    logger.stop().unwrap()

def test_print_recovers_from_stdout_failure(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    original_path = builtins.print

    class PrintCounter:
        def __init__(self) -> None:
            self.counter = 0

    print_counter = PrintCounter()

    def flaky_print(*args: Any, **kwargs: Any) -> None:
        if print_counter.counter == 0:
            print_counter.counter += 1
            raise RuntimeError("Simulated stdout failure")
        return original_path(*args, **kwargs)

    monkeypatch.setattr(builtins, "print", flaky_print)

    logger = AsyncLogger()
    logger.start().unwrap()

    result = logger.print("Trigger fallback", LogType.INFO)
    assert isinstance(result, Success)

    logger.stop().unwrap()

    captured = capsys.readouterr()
    assert "Print failed" in captured.err

def test_queue_overflow_and_metrics(monkeypatch: pytest.MonkeyPatch) -> None:
    logger = AsyncLogger(max_queue_size=1)

    def mock_put_nowait(_item: Any) -> None:
        raise queue.Full()

    monkeypatch.setattr(logger._queue,  # pyright: ignore[reportPrivateUsage]
                        "put_nowait",
                        mock_put_nowait,
                        raising=True)
    
    result = logger.log("OVERFLOW", LogType.INFO)
    assert isinstance(result, Failure)
    assert isinstance(result.failure(), RuntimeError)

    assert logger.dropped_count().unwrap() == 1

    assert logger.reset_metrics().unwrap() is True
    assert logger.dropped_count().unwrap() == 0

# Metrics and Counters ----------------------------------------------------------------------------------------------------------

def test_dropped_counter_increment(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(max_queue_size=1, output_fn=fn)
    logger.start().unwrap()

    assert logger.log("Message 1").unwrap() is True  # Enqueue
    result = logger.log("Message 2")  # Should drop due to overflow
    assert isinstance(result, Failure)  # Should be a Failure due to queue overflow
    
    dropped = logger.dropped_count().unwrap()
    assert dropped == 1  # One message dropped

    # Reset and check again
    assert logger.reset_metrics().unwrap() is True  # Reset metrics
    assert logger.dropped_count().unwrap() == 0  # Should be reset
    logger.stop().unwrap()

# Stress without Wall-clock Sleep -----------------------------------------------------------------------------------------------

def test_high_volume_burst(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(max_queue_size=500000, flush_interval=0.01, output_fn=fn)
    logger.start().unwrap()

    # Burst of 5000000 small messages - some may be dropped due to queue overflow
    successful_logs = 0
    total_attempts = 5000000
    for i in range(total_attempts):
        result = logger.log(f"Message {i}")
        if isinstance(result, Success):
            successful_logs += 1
        # If result is Failure, it means queue overflow - that's expected behavior

    logger.stop().unwrap()
    # Check that we processed at least the queue size worth of messages
    assert hits["count"] >= 500000  # At least queue size messages should be processed
    assert successful_logs + logger.dropped_count().unwrap() == total_attempts  # Total should match

# Concurrency - Rate Stress -----------------------------------------------------------------------------------------------------

def test_parallel_logging_threads(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(output_fn=fn)
    logger.start().unwrap()

    def spam(n: int) -> None:
        for _ in range(n):
            logger.log("X")  # Don't unwrap, let queue full errors be handled gracefully

    threads = [threading.Thread(target=spam, args=(5000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()

    logger.stop().unwrap()
    assert hits["count"] + logger.dropped_count().unwrap() == 20000  # Total should match

# Real-time Behavior -------------------------------------------------------------------------------------------------------------

def test_auto_restart_after_sink_fault(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(output_fn=fn, flush_interval=0.05)
    logger.start().unwrap()

    hits["fail_next"] = True  # Force first log to fail
    logger.log("BOOM").unwrap()

    deadline = time.time() + 2.0
    original_worker = logger._worker_thread  # pyright: ignore[reportPrivateUsage]
    while time.time() < deadline:
        if logger._state_lock:  # pyright: ignore[reportPrivateUsage]
            if logger._worker_thread is not original_worker and logger.is_running:  # pyright: ignore[reportPrivateUsage]
                break
        time.sleep(0.05)

    assert logger.is_running
    logger.log("Recovered").unwrap()
    logger.stop().unwrap()

def test_graceful_shutdown_timeout(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn, flush_interval=0.05)
    logger.start().unwrap()

    # Enqueue slow task to push shutdown logic
    for _ in range(100):
        logger.log("Slow task").unwrap()

    t0 = time.perf_counter()
    assert logger.stop(timeout=0.1).unwrap() is True  # Should succeed
    elapsed = time.perf_counter() - t0
    # Shutdown should respect provided timeout budget
    assert elapsed < 5.0

# Pathological Edge-case --------------------------------------------------------------------------------------------------------

def test_supervisor_backoff_does_not_exceed_max(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, hits = sink_counter
    logger = AsyncLogger(output_fn=fn, flush_interval=0.05)
    logger.start().unwrap()

    for _ in range(5):
        hits["fail_next"] = True
        logger.log("Crash").unwrap()
        time.sleep(0.05)

    assert logger._restart_backoff <= 30  # pyright: ignore[reportPrivateUsage]
    logger.stop().unwrap()

def test_start_blocks_until_finishes(sink_counter: Tuple[OutputFn, HitsDict]) -> None:
    fn, _ = sink_counter
    logger = AsyncLogger(output_fn=fn, flush_interval=0.05)
    logger.start().unwrap()

    started_stop = threading.Event()
    def _call_stop():
        started_stop.set()
        logger.stop().unwrap()
    t = threading.Thread(target=_call_stop)
    t.start()

    started_stop.wait()
    time.sleep(0.02) # Let STOPPING state exsist for a bit
    result = logger.start()
    assert isinstance(result, Success) and result.unwrap() is True  # Should be idempotent

    logger.stop().unwrap()
    t.join()

def test_start_failure_path(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_sink: OutputFn = lambda msg, lvl: Success("OK")
    logger = AsyncLogger(output_fn=fake_sink)

    def boom(self: threading.Thread) -> None:
        raise RuntimeError("BOOM")
    monkeypatch.setattr(threading.Thread, "start", boom)

    result = logger.start()
    assert isinstance(result, Failure)
    assert logger._state is WorkerState.STOPPED  # pyright: ignore[reportPrivateUsage]

def test_stop_when_queue_full(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_sink: OutputFn = lambda msg, lvl: Success("OK")
    logger = AsyncLogger(output_fn=fake_sink, max_queue_size=1, flush_interval=0.05)
    logger.start().unwrap()
    logger.log("Only slot").unwrap()  # Fill queue

    def mock_put_nowait(_item: object) -> None:
        raise queue.Full()

    monkeypatch.setattr(
        logger._queue,  # pyright: ignore[reportPrivateUsage]
        "put_nowait",
        mock_put_nowait
    )

    assert logger.stop(timeout=1.0).unwrap() is True  # Should succeed even with full queue
    assert not logger.is_running  # Should be stopped

def test_strat_waits_if_stop_in_progress() -> None:
    def delayed_sink(msg: str, lvl: LogType) -> Result[str, Exception]:
        time.sleep(0.05)
        return Success("OK")
    
    logger = AsyncLogger(output_fn=delayed_sink, flush_interval=0.01, max_queue_size=10)
    logger.start().unwrap()

    for i in range(3):
        logger.log(f"Warm-up message {i}").unwrap()

    stop_begin = threading.Event()
    def _call_stop():
        stop_begin.set()
        logger.stop(timeout=2.0).unwrap()
    t = threading.Thread(target=_call_stop)
    t.start()
    stop_begin.wait()
    time.sleep(0.01)  # Ensure stop is in progress

    t0 = time.perf_counter()
    result = logger.start()
    elapsed = time.perf_counter() - t0

    assert result.unwrap() is True
    assert elapsed >= 0.03

    logger.stop().unwrap()
    t.join()

# ========================================================= END OF FILE =========================================================
