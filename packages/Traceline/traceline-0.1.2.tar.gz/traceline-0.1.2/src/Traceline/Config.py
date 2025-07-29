# ──────────────────────────────────────────────────────────────────────────────────────
#                              TRACELINE CONFIGURATION CORE
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : Config.py
#     Module Name    : Traceline Configuration Core
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.2
#
# FILE DESCRIPTION:
#     Configuration management system for Traceline Logger with hierarchical
#     resolution (overrides > environment variables > defaults). Provides
#     type-safe configuration loading with automatic .env file support.
#
# PROGRAM DESCRIPTION:
#     Primary Features:
#       • Hierarchical configuration resolution with fallback chain
#       • Type-safe schema validation using TypedDict
#       • Environment variable parsing with automatic type conversion
#       • .env file support via python-dotenv
#       • Immutable configuration objects with Result-based error handling
#       • Built-in validation and bounds checking for numeric values
#       • Boolean parsing from multiple string formats
#
# SECURITY CONSIDERATIONS:
#     • Environment variables may expose sensitive configuration data
#     • Configuration values are validated and bounded to prevent attacks
#     • No arbitrary code execution in configuration parsing
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : os, typing, collections.abc, returns, python-dotenv
#
# USAGE:
#     >>> from traceline import get_config
#     >>> config = get_config().unwrap()
#     >>> print(config["logger_name"])  # "HYRA-0"
#     >>> 
#     >>> # With environment variables
#     >>> os.environ["LOGGER_NAME"] = "MyApp"
#     >>> config = get_config().unwrap()
#     >>> 
#     >>> # With explicit overrides
#     >>> overrides = {"LOGGER_NAME": "TestApp", "LOG_LEVEL": "DEBUG"}
#     >>> config = get_config(overrides).unwrap()
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

import os

from typing import Final, Optional, TypedDict, Any
from collections.abc import Mapping
from returns.result import Result, Success, Failure
from dotenv import load_dotenv
from .Types import LogType

load_dotenv()

class ConfigSchema(TypedDict):
    logger_name: str
    log_level: LogType
    flush_interval: float
    max_queue_size: int
    cache_enabled: bool

_DEFAULTS: Final[ConfigSchema] = {
    "logger_name": "HYRA-0",
    "log_level": LogType.INFO,
    "flush_interval": 0.5,
    "max_queue_size": 10000,
    "cache_enabled": True
}

_ENV_KEYS: Final[dict[str, str]] = {
    "logger_name": "LOGGER_NAME",
    "log_level": "LOG_LEVEL",
    "flush_interval": "FLUSH_INTERVAL",
    "max_queue_size": "MAX_QUEUE_SIZE",
    "cache_enabled": "LOG_CACHE"
}

_BOOL_MAP: Final[dict[str, bool]] = {
    "1": True, "true": True, "yes": True, "on": True,
    "0": False, "false": False, "no": False, "off": False,
}
def get_config(overrides: Optional[Mapping[str, str]] = None) -> Result[ConfigSchema, str]:
    """
    Resolves configuration from (overrides > env > defaults) in a deterministic
    and testable manner. Does not mutate global state.

    Args:
        overrides (Optional[dict[str, str]]): Optional injection layer.

    Returns:
        Result[ConfigSchema, Exception]
    """
    try:
        source = overrides or os.environ
        cfg = {}

        cfg["logger_name"] = _resolve("logger_name", str, source).value_or(_DEFAULTS["logger_name"])

        # Log Level
        log_level_str = _resolve("log_level", str, source).value_or(_DEFAULTS["log_level"].name)
        log_level = LogType.from_str(log_level_str).value_or(_DEFAULTS["log_level"])
        cfg["log_level"] = log_level

        # Flush Interval
        flush = _resolve("flush_interval", float, source).value_or(_DEFAULTS["flush_interval"])
        cfg["flush_interval"] = max(0.01, flush)

        # Queue Size
        queue = _resolve("max_queue_size", int, source).value_or(_DEFAULTS["max_queue_size"])
        cfg["max_queue_size"] = max(10, queue)

        # Cache Enabled
        raw = _resolve("cache_enabled", str, source).value_or(str(_DEFAULTS["cache_enabled"]))
        cfg["cache_enabled"] = _BOOL_MAP.get(raw.strip().lower(), _DEFAULTS["cache_enabled"])

        return Success(cfg)  # type: ignore

    except Exception as e:
        return Failure(str(e))
    
def _resolve(key: str, type_: type, source: Mapping[str, str]) -> Result[Any, Exception]:
    """
    Safely resolve and cast a configuration value from the provided source.
    Supports string→int/float/bool conversions.

    Returns:
        Result[T, Exception]
    """
    env_key = _ENV_KEYS.get(key)
    if not env_key or env_key not in source:
        return Failure(KeyError(f"{key} not found in source"))
    
    raw = source[env_key]

    try:
        if type_ is str:
            return Success(raw.strip())
        elif type_ is int:
            return Success(int(raw.strip()))
        elif type_ is float:
            return Success(float(raw.strip()))
        else:
            return Failure(TypeError(f"Unsupported type for {key}"))
    except Exception as e:
        return Failure(e)
    
# ========================================================= END OF FILE =========================================================
