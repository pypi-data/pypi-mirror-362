# ──────────────────────────────────────────────────────────────────────────────────────
#                           TRACELINE CONFIGURATION CORE TESTS
#                              (Comprehensive Unit Tests)
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : test_Config.py
#     Module Name    : Traceline Configuration Core Tests
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.2
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
#     Last Updated   : 2025‑07‑10
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

import os
import pytest
import importlib
from typing import Any

from returns.result import Failure
from pathlib import Path

from Traceline.Types import LogType

import Traceline.Config as Config

# Utility Helpers ---------------------------------------------------------------------------------------------------------------

def _clear_env() -> None:
    """
    Remove every environment variable the config loader understands.
    """
    for key in Config._ENV_KEYS.values():  # pyright: ignore[reportPrivateUsage]
        os.environ.pop(key, None)

def _reload() -> Any:
    return importlib.reload(Config)

# Positive Path for get_config --------------------------------------------------------------------------------------------------

def test_defaults_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env()
    cfg = Config.get_config().unwrap()
    assert cfg == Config._DEFAULTS  # pyright: ignore[reportPrivateUsage]

def test_overrides_full_customisation() -> None:
    overrides: dict[str, str] = {
        "LOGGER_NAME": "TestLogger",
        "LOG_LEVEL": "DEBUG",
        "FLUSH_INTERVAL": "1.5",
        "MAX_QUEUE_SIZE": "500",
        "LOG_CACHE": "false"
    }
    cfg = Config.get_config(overrides).unwrap()

    assert cfg["logger_name"] == "TestLogger"
    assert cfg["log_level"] == LogType.DEBUG
    assert cfg["flush_interval"] == 1.5
    assert cfg["max_queue_size"] == 500
    assert cfg["cache_enabled"] is False

@pytest.mark.parametrize("token, value", Config._BOOL_MAP.items())  # pyright: ignore[reportPrivateUsage]
def test_bool_variants(token: str, value: bool) -> None:
    overrides: dict[str, str] = {"LOG_CACHE": token}
    cfg = Config.get_config(overrides).unwrap()
    assert cfg["cache_enabled"] is value

def test_value_clamping() -> None:
    overrides: dict[str, str] = {"FLUSH_INTERVAL": "0", "MAX_QUEUE_SIZE": "5"}
    cfg = Config.get_config(overrides).unwrap()
    assert cfg["flush_interval"] == pytest.approx(0.01)  # type: ignore[misc]
    assert cfg["max_queue_size"] == 10


def test_fallback_on_invalid_log_level() -> None:
    overrides: dict[str, str] = {"LOG_LEVEL": "BOGUS"}
    cfg = Config.get_config(overrides).unwrap()
    assert cfg["log_level"] == Config._DEFAULTS["log_level"]  # pyright: ignore[reportPrivateUsage]

# _resolve Utility - Success and Failure Branches -------------------------------------------------------------------------------

def test_resolve_success_all_types() -> None:
    src = {
        "LOGGER_NAME": "UnitTest",
        "MAX_QUEUE_SIZE": "123",
        "FLUSH_INTERVAL": "2.34"
    }

    assert Config._resolve("logger_name", str, src).unwrap() == "UnitTest"  # pyright: ignore[reportPrivateUsage]
    assert Config._resolve("max_queue_size", int, src).unwrap() == 123  # pyright: ignore[reportPrivateUsage]
    assert Config._resolve("flush_interval", float, src).unwrap() == pytest.approx(2.34)  # type: ignore[misc]

def test_resolve_missing_key() -> None:
    with pytest.raises(Exception):
        Config._resolve("logger_name", str, {}).unwrap()  # pyright: ignore[reportPrivateUsage]

def test_resolve_bad_cast() -> None:
    bad_int = { "MAX_QUEUE_SIZE": "not_an_int" }
    with pytest.raises(Exception):
        Config._resolve("max_queue_size", int, bad_int).unwrap()  # pyright: ignore[reportPrivateUsage]

def test_resolve_unsupported_type() -> None:
    src = { "LOGGER_NAME": "irrelevant" }
    result = Config._resolve("logger_name", bool, src)  # pyright: ignore[reportPrivateUsage]
    
    # Check that unwrap() raises an exception and that the original cause is TypeError
    with pytest.raises(Exception) as exc_info:
        result.unwrap()
    
    # The exception should have a __cause__ that is a TypeError
    assert isinstance(exc_info.value.__cause__, TypeError)

# Force the Exception Arm Inside get_config -------------------------------------------------------------------------------------

def test_get_config_exception_path(monkeypatch: pytest.MonkeyPatch) -> None:
    def _bomb(*_args: Any, **_kwargs: Any) -> None:
        raise RuntimeError("BOOM")

    monkeypatch.setattr(Config, "_resolve", _bomb, raising=True)
    failure = Config.get_config()
    assert isinstance(failure, Failure)
    assert "BOOM" in failure.failure()

# Verify Module-Level Excution Survives Reload ----------------------------------------------------------------------------------

def test_module_import_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_env = tmp_path / ".env"
    fake_env.touch()
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    again = _reload()
    assert hasattr(again, "get_config")
    assert again._DEFAULTS["logger_name"] == "HYRA-0"  # pyright: ignore[reportPrivateUsage]
