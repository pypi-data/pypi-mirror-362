# ──────────────────────────────────────────────────────────────────────────────────────
#                               TRACELINE LOGGER TESTS
#                              (Comprehensive Unit Tests)
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : test_Logger.py
#     Module Name    : Traceline Logger Tests
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.1
#
# SYSTEM INTEGRATION:
#     Part of        : HYRA‑0 – Zero‑Database Mathematical & Physical Reasoning Engine
#     Subsystem      : Traceline Logging Core
#
# MAINTAINABILITY:
#     Author         : Michael Tang
#     Organization   : BioNautica Research Initiative
#     Contact        : michaeltang@bionautica.org
#     Created        : 2025‑07‑08
#     Last Updated   : 2025‑07‑09
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import pytest

from typing import Callable, Generator, Dict, Any
from returns.result import Success, Failure, Result

import Traceline

from Traceline.Logger import LoggerBuilder, get_logger, _LOGGER_CACHE  # pyright: ignore[reportPrivateUsage]
from Traceline.Types import LogType

# Common Fake Logger Sink --------------------------------------------------------------------------------------------------------

class DummyLogger:
    def __init__(self, 
                 name: str,
                 loglevel: LogType,
                 flush_interval: float,
                 max_queue_size: int,
                 output_fn: Callable[[str, LogType], Result[str, Exception]]):
        self.name = name
        self.loglevel = loglevel
        self.flush_interval = flush_interval
        self.max_queue_size = max_queue_size
        self.output_fn = output_fn

    def start(self):
        return Success(True)
    
    def log(self, *_):
        return Success(True)
    
    def stop(self, *_):
        return Success(True)
    
# Fixture ------------------------------------------------------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_cache() -> Generator[None, None, None]:
    _LOGGER_CACHE.clear()
    yield
    _LOGGER_CACHE.clear()

# Test Cases ---------------------------------------------------------------------------------------------------------------------

def test_get_logger_caches(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(Traceline.Logger, "AsyncLogger", DummyLogger)
    first = get_logger("CacheApp")
    second = get_logger("CacheApp")
    assert first is second
    assert list(_LOGGER_CACHE) == ["CacheApp"]

def test_builder_custom_config(monkeypatch: pytest.MonkeyPatch):
    captured: Dict[str, Any] = {}

    class CaptureLogger(DummyLogger):
        def __init__(self, 
                     name: str,
                     loglevel: LogType,
                     flush_interval: float,
                     max_queue_size: int,
                     output_fn: Callable[[str, LogType], Result[str, Exception]]):
            super().__init__(
                name=name,
                loglevel=loglevel,
                flush_interval=flush_interval,
                max_queue_size=max_queue_size,
                output_fn=output_fn
            )
            captured["name"] = name
            captured["loglevel"] = loglevel
            captured["flush_interval"] = flush_interval
            captured["max_queue_size"] = max_queue_size
            captured["output_fn"] = output_fn

    monkeypatch.setattr(Traceline.Logger, "AsyncLogger", CaptureLogger)

    backend: Callable[[str, LogType], Result[str, Exception]] = lambda m, t: Success("OK")

    (
        LoggerBuilder()
        .with_name("CustomApp")
        .with_level(LogType.DEBUG)
        .with_flush_interval(0)
        .with_max_queue_size(5)
        .with_backend(backend)
        .without_cache()
        .build()
        .unwrap()
    )

    assert captured["name"] == "CustomApp"
    assert captured["loglevel"] == LogType.DEBUG
    assert captured["flush_interval"] == 0.01  # Minimum enforced by builder
    assert captured["max_queue_size"] == 10     # Minimum enforced by builder
    assert captured["output_fn"] == backend
    assert "CustomApp" not in _LOGGER_CACHE

def test_builder_cache_hit(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(Traceline.Logger, "AsyncLogger", DummyLogger)\
    
    builder = LoggerBuilder().with_name("CacheHit")
    first = builder.build().unwrap()
    again = builder.build()

    assert isinstance(again, Success)
    assert again.unwrap() is first

def test_builder_rebuild(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(Traceline.Logger, "AsyncLogger", DummyLogger)

    builder = LoggerBuilder().with_name("RebuildTest")
    old = builder.build().unwrap()
    new = builder.rebuild().unwrap()

    assert new is not old
    # Rebuild will rewrite the cache entry
    assert "RebuildTest" in _LOGGER_CACHE

def test_builder_start_failure(monkeypatch: pytest.MonkeyPatch):
    class FailingLogger(DummyLogger):
        def start(self) -> Failure[RuntimeError]:  # pyright: ignore[reportIncompatibleMethodOverride]
            return Failure(RuntimeError("Boot failure"))
        
    monkeypatch.setattr(Traceline.Logger, "AsyncLogger", FailingLogger)

    result = LoggerBuilder().with_name("BOOM").build()
    assert isinstance(result, Failure)
    assert "Boot failure" in str(result.failure())
    # Failure to build should not dirty the cache
    assert "BOOM" not in _LOGGER_CACHE

# ========================================================= END OF FILE =========================================================
