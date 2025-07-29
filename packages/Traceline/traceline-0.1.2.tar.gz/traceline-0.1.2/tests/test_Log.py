# ──────────────────────────────────────────────────────────────────────────────────────
#                             TRACELINE LOG FORMATTER TESTS
#                              (Comprehensive Unit Tests)
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : test_Log.py
#     Module Name    : Traceline Log Formatter Tests
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
#     Created        : 2025‑07‑09
#     Last Updated   : 2025‑07‑09
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import builtins
import pytest
from pathlib import Path
from typing import Any, Callable, IO
import Traceline.Log as Log

from returns.result import Success, Failure
from Traceline.Types import LogType, Color

# Helper ------------------------------------------------------------------------------------------------------------------------

def _open_stub_factory(failure: int) -> Callable[..., IO[Any]]:
    """
    Return a replacement for builtins.open that throws OSError failures times
    then delegates to the real open(). Used to hit the retry loop.
    """
    real_open = builtins.open
    counter = { "n": 0 }

    def _open(*args: Any, **kwargs: Any) -> IO[Any]:
        if counter["n"] < failure:
            counter["n"] += 1
            raise OSError("BOOM")
        return real_open(*args, **kwargs)  # type: ignore[return-value]
    
    return _open

# Sanitize Message Tests ---------------------------------------------------------------------------------------------------------

def test_sanitize_success() -> None:
    result = Log._sanitize_message("Hello\nWorld!")  # pyright: ignore[reportPrivateUsage]
    assert isinstance(result, Success)
    assert result.unwrap() == "Hello\\nWorld!"

@pytest.mark.parametrize(
    "bad", [ "   \t  ", "x" * 1025], ids=["whitespace", "too-long" ]
)
def test_sanitize_failure(bad: str) -> None:
    result = Log._sanitize_message(bad)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(result, Failure)
    assert isinstance(result.failure(), ValueError)

# Log Format Tests --------------------------------------------------------------------------------------------------------------

def test_format_log_success() -> None:
    out = Log._format_log("Message", LogType.SUCCESS).unwrap()  # pyright: ignore[reportPrivateUsage]
    assert "[SUCCESS]" in out and Color.RESET.value in out

def test_format_log_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "get_color", lambda _: Failure(ValueError("No color")), raising=True)  # type: ignore[arg-type]
    assert isinstance(Log._format_log("X", LogType.INFO), Failure)  # pyright: ignore[reportPrivateUsage]

# Resolve Log File Name Tests ---------------------------------------------------------------------------------------------------

def test_resolve_no_rotation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    monkeypatch.setattr(Log, "MAX_LOG_SIZE_BYTES", 100, raising=True)

    base = "run"
    f = tmp_path / f"{base}.log"
    f.write_text("OK")
    assert Log._resolve_log_filename(base) == f  # pyright: ignore[reportPrivateUsage]

def test_resolve_with_rotation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    monkeypatch.setattr(Log, "MAX_LOG_SIZE_BYTES", 1, raising=True)

    base = "rotate"
    (tmp_path / f"{base}.log").write_bytes(b"XX")
    rotated = Log._resolve_log_filename(base)  # pyright: ignore[reportPrivateUsage]
    assert rotated.name == f"{base}001.log"

# Write Log Tests ---------------------------------------------------------------------------------------------------------------

def test_write_log_dir_not_writable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    
    def mock_access(path: Any, mode: Any) -> bool:
        return False
    
    monkeypatch.setattr(Log.os, "access", mock_access, raising=True)

    result = Log._write_log("Locked", LogType.WARNING)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(result, Failure) and isinstance(result.failure(), PermissionError)

def test_write_log_retry_then_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    
    def mock_fsync(fd: Any) -> None:
        pass
    
    def mock_sleep(t: Any) -> None:
        pass
    
    monkeypatch.setattr(Log.os, "fsync", mock_fsync, raising=True)
    monkeypatch.setattr(Log.time, "sleep", mock_sleep, raising=True)
    monkeypatch.setattr(builtins, "open", _open_stub_factory(1), raising=True)

    res = Log._write_log("Retry", LogType.DEBUG)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(res, Success)
    assert any("Retry" in p.read_text() for p in tmp_path.glob("*.log"))

def test_write_log_exhaust_retries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    
    def mock_fsync(fd: Any) -> None:
        pass
    
    def mock_sleep(t: Any) -> None:
        pass
    
    def mock_open_always_fail(*args: Any, **kwargs: Any) -> Any:
        raise OSError("BOOM")
    
    monkeypatch.setattr(Log.os, "fsync", mock_fsync, raising=True)
    monkeypatch.setattr(Log.time, "sleep", mock_sleep, raising=True)
    monkeypatch.setattr(builtins, "open", mock_open_always_fail, raising=True)

    result = Log._write_log("Fail", LogType.ERROR)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(result, Failure) and isinstance(result.failure(), OSError)

def test_write_log_outer_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_mkdir_fail(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("BOOM")
    
    monkeypatch.setattr(Path, "mkdir", mock_mkdir_fail, raising=True)
    result = Log._write_log("OOPS", LogType.INFO)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(result, Failure) and isinstance(result.failure(), RuntimeError)

# High-Level Log Tests ----------------------------------------------------------------------------------------------------------

def test_log_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Log, "LOG_DIR", tmp_path, raising=True)
    
    def mock_fsync(fd: Any) -> None:
        pass
    
    monkeypatch.setattr(Log.os, "fsync", mock_fsync, raising=True)

    result = Log.log("TOP-LEVEL", LogType.MESSAGE)
    assert isinstance(result, Success) and "[INFO]" in result.unwrap()

def test_log_failure_bubbles(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_write_log_fail(m: Any, l: Any) -> Failure[IOError]:
        return Failure(IOError("DOWNSTREAM"))
    
    monkeypatch.setattr(Log, "_write_log", mock_write_log_fail, raising=True)
    result = Log.log("BUBBLE", LogType.INFO)
    assert isinstance(result, Failure) and isinstance(result.failure(), IOError)

# ========================================================= END OF FILE =========================================================
