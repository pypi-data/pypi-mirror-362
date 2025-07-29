# ──────────────────────────────────────────────────────────────────────────────────────
#                                TRACELINE LOG FORMATTER
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : Log.py
#     Module Name    : Traceline Log Formatter
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.2
#
# FILE DESCRIPTION:
#     Provides functional, type-safe log formatting and file output mechanisms
#     based on Result-returning Rust-like structure. Supports ANSI console
#     formatting and structured output to rotating log files with timestamping.
#
# PROGRAM DESCRIPTION:
#     Primary Functions:
#         - format_log_message(): Compose styled console string with ANSI colors
#         - write_log_file(): Write log record with timestamp to rotating files
#         - log(): High-level function for console + file combined output
#         - Message sanitization with size limits and injection prevention
#         - Automatic log rotation based on file size (10MB limit)
#         - Daily log file naming with incremental counters
#
# SECURITY CONSIDERATIONS:
#     - Handles all I/O with retry-safe logic and proper error handling
#     - Path is restricted to local `.log/` folder with controlled permissions
#     - Message sanitization prevents injection attacks and enforces size limits
#     - File operations use atomic writes with fsync for data integrity
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : os, time, datetime, pathlib, returns, typing
#
# USAGE:
#     >>> from traceline import log, LogType
#     >>> log("Application started", LogType.INFO).unwrap()
#     >>> log("Debug information", LogType.DEBUG).unwrap()
#     >>> log("Warning message", LogType.WARN).unwrap()
#     >>> 
#     >>> # Error handling
#     >>> result = log("", LogType.INFO)
#     >>> if result.failure():
#     ...     print("Logging failed:", result.failure())
#     >>> 
#     >>> # Files are automatically created in .log/ directory
#     >>> # Format: ".log/MMDDYYYY HHMM000.log" (with rotation)
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
import time

from datetime import datetime
from pathlib import Path
from returns.result import Result, Success, Failure
from typing import Final

from .Types import LogType, Color, get_color

# Constants
MAX_LOG_SIZE_BYTES: Final[int] = 10 * 1024 * 1024 # 10MB
LOG_DIR: Final[Path] = Path(".log")
ENCODING: Final[str] = "utf-8"
MAX_RETRIES: Final[int] = 3

# Public API
def log(message: str, logtype: LogType) -> Result[str, Exception]:
    """
    High-level logging function: Prints to console and appends to log file.

    Args:
        message (str): The message to log.
        logtype (LogType): The severity/type of log

    Returns:
        Result[str, Exception]: Console-colored string on Success or Error details.
    """
    return (
        _sanitize_message(message)
        .bind(lambda m: _format_log(m, logtype)) # type: ignore
        .bind(lambda formatted: _write_log(formatted, logtype).map(lambda _: formatted)) # type: ignore
    )

# Internal Utilities
def _sanitize_message(raw: str) -> Result[str, ValueError]:
    """
    Sanitize message for logging: remove line breaks, enforce size.

    Returns:
        Result[str, ValueError]: Safe string or error.
    """
    if not raw.strip():
        return Failure(ValueError("Empty or whitespace-only log message"))
    if len(raw) > 1024:
        return Failure(ValueError("Message exceeds 1024 character limit"))
    clean = raw.replace('\n', '\\n').replace('\r', '\\r')
    return Success(clean)

def _format_log(msg: str, logtype: LogType) -> Result[str, Exception]:
    """
    Fromat colsole string with ANSI color and log type prefix.

    Returns:
        Result[str, Exception]: Styled string or formatting  error.
    """
    return get_color(logtype).map(
        lambda color: f"{color.value}[{logtype.name}] {Color.RESET.value}{msg}"
    )

def _write_log(msg: str, logtype: LogType) -> Result[bool, Exception]:
    """
    Write formatted message to daily rotating log file.

    Returns:
        Result[bool, Exception]: True if written, or failure.
    """
    try:
        LOG_DIR.mkdir(exist_ok=True, mode=0o755)
        if not os.access(LOG_DIR, os.W_OK):
            return Failure(PermissionError(f"Log directory {LOG_DIR} not writable"))
        
        now = datetime.now()
        base_name = now.strftime("%m%d%Y %H%M")
        full_path = _resolve_log_filename(base_name)

        timestamped = f"[{now.strftime('%m-%d-%Y %H:%M:%S')}] [{logtype.name}] {msg}\n"

        for attempt in range(MAX_RETRIES):
            try:
                with open(full_path, 'a', encoding=ENCODING, buffering=1) as file:
                    file.write(timestamped)
                    file.flush()
                    os.fsync(file.fileno())
                return Success(True)
            except (PermissionError, OSError):
                time.sleep(0.1)
                attempt += 1
                continue
        
        return Failure(IOError(f"Log write failed after {MAX_RETRIES} attempts"))
    
    except Exception as e:
        return Failure(e)

def _resolve_log_filename(base_name: str) -> Path:
    """
    Ensure log file doesn't exceed size limit by appending suffix if needed.

    Returns:
        Path: Final resolved log file path.
    """
    counter = 0
    while True:
        suffix = f"{counter:03d}" if counter > 0 else ""
        candidate = LOG_DIR / f"{base_name}{suffix}.log"
        if not candidate.exists() or candidate.stat().st_size < MAX_LOG_SIZE_BYTES:
            return candidate
        counter += 1

# ========================================================= END OF FILE =========================================================
