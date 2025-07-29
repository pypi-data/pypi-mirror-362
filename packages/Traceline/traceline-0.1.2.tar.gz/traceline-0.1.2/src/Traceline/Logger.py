# ──────────────────────────────────────────────────────────────────────────────────────
#                               TRACELINE LOGGER FACTORY
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : Logger.py
#     Module Name    : Traceline Logger Factory
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.3
#
# FILE DESCRIPTION:
#     Provides a singleton factory interface for creating and caching AsyncLogger
#     instances with default or customized configurations. Uses Builder pattern
#     to support deferred initialization and environment-driven log level setup.
#
# PROGRAM DESCRIPTION:
#     Primary Functions:
#         - get_logger(): Top-level factory function for singleton logger access
#         - LoggerBuilder: Fluent API for customized logger configuration
#         - _LOGGER_CACHE: Internal singleton cache ensuring one logger per name
#         - Environment-driven configuration with LOG_LEVEL support
#         - Automatic logger startup and error handling via Result types
#
# SECURITY CONSIDERATIONS:
#     - Logger cache prevents memory leaks through controlled singleton access
#     - Environment variable parsing is sanitized and bounded
#     - Builder pattern prevents invalid configuration states
#     - Automatic cleanup of failed logger instances
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : os, typing, returns, AsyncLogger, LogType, Log
#
# USAGE:
#     >>> from traceline import get_logger, LoggerBuilder, LogType
#     >>> 
#     >>> # Simple factory usage
#     >>> logger = get_logger("MyApp")
#     >>> logger.log("Hello world", LogType.INFO)
#     >>> 
#     >>> # Advanced builder pattern
#     >>> custom_logger = (LoggerBuilder()
#     ...     .with_name("CustomApp")
#     ...     .with_level(LogType.DEBUG)
#     ...     .with_flush_interval(1.0)
#     ...     .with_max_queue_size(5000)
#     ...     .without_cache()
#     ...     .build().unwrap())
#     >>> 
#     >>> # Rebuild existing logger
#     >>> rebuilt = LoggerBuilder().with_name("MyApp").rebuild().unwrap()
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

from typing import Callable, Final
from returns.result import Result, Success, Failure

from .Types import LogType
from .AsyncLogger import AsyncLogger
from .Log import log as default_log_func

# Internal Logger Cache
_LOGGER_CACHE: dict[str, AsyncLogger] = {}

# Default Config Values
DEFAULT_LOGGER_NAME: Final[str] = "HYRA-0 Traceline Logger"
DEFAULT_LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO").strip().upper()

# Public API
def get_logger(name: str = DEFAULT_LOGGER_NAME) -> AsyncLogger:
    """
    Return a cached AsyncLogger or construct it via default config.

    Args:
        name (str): Unique logger name identifier.

    Returns:
        AsyncLogger: Logger instance
    """
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]
    
    return (
        LoggerBuilder()
        .with_name(name)
        .build()
        .unwrap()
    )

# Builder Class
class LoggerBuilder():
    """
    LoggerBuilder provides a type-safe, fully customizable configuration flow
    for constructing AsyncLogger instances.
    """
    def __init__(self) -> None:
        level_result = LogType.from_str(DEFAULT_LOG_LEVEL)
        self._name: str = DEFAULT_LOGGER_NAME
        self._level: LogType = level_result.value_or(LogType.INFO)
        self._interval: float = 0.5
        self._max_queue: int = 10000
        self._backend: Callable[[str, LogType], Result[str, Exception]] = default_log_func
        self._use_cache: bool = True

    def with_name(self, name: str) -> "LoggerBuilder":
        self._name = name.strip()
        return self
    
    def with_level(self, level: LogType) -> "LoggerBuilder":
        self._level = level
        return self
    
    def with_flush_interval(self, interval: float) -> "LoggerBuilder":
        self._interval = max(0.01, interval)
        return self
    
    def with_max_queue_size(self, size: int) -> "LoggerBuilder":
        self._max_queue = max(10, size)
        return self
    
    def with_backend(self, func: Callable[[str, LogType], Result[str, Exception]]) -> "LoggerBuilder":
        self._backend = func
        return self
    
    def without_cache(self) -> "LoggerBuilder":
        self._use_cache = False
        return self
    
    def build(self) -> Result[AsyncLogger, Exception]:
        """
        Instantiate AsyncLogger with full configuration.

        Returns:
            Result[AsyncLogger, Exception]
        """
        try:
            if self._use_cache and self._name in _LOGGER_CACHE:
                return Success(_LOGGER_CACHE[self._name])
            
            logger = AsyncLogger(
                name=self._name,
                loglevel=self._level,
                flush_interval=self._interval,
                max_queue_size=self._max_queue,
                output_fn=self._backend
            )

            result = logger.start()
            if isinstance(result, Failure):
                raise result.failure()
            
            if self._use_cache:
                _LOGGER_CACHE[self._name] = logger

            return Success(logger)
        
        except Exception as e:
            return Failure(e)
        
    def rebuild(self) -> Result[AsyncLogger, Exception]:
        """
        Force reconstruction and override existing logger instance.

        Returns:
            Result[AsyncLogger, Exception]
        """
        self._use_cache = True
        if self._name in _LOGGER_CACHE:
            del _LOGGER_CACHE[self._name]
        return self.build()
    
# ========================================================= END OF FILE =========================================================
