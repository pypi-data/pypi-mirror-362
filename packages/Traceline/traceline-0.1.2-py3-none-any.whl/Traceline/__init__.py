# ──────────────────────────────────────────────────────────────────────────────────────
#                                TRACELINE LOGGER CORE
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : __init__.py
#     Module Name    : Traceline Logger Core
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.3
#
# FILE DESCRIPTION:
#     Package initialization file that exports the public API for the Traceline Logger
#     Core. This module serves as the main entry point for importing logging
#     functionality, type definitions, configuration, and utilities.
#
# PROGRAM DESCRIPTION:
#     Primary Features:
#       • Exports core logger classes (Logger, AsyncLogger, LoggerBuilder)
#       • Provides type system definitions (LogType, Color, get_color)
#       • Exposes configuration management (get_config)
#       • Includes log formatting utilities (log)
#       • Creates default singleton logger instance for immediate use
#
# SECURITY CONSIDERATIONS:
#     • Logger instances handle sensitive data - ensure proper access controls
#     • Configuration loading may expose system paths and settings
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : Internal modules (Logger, AsyncLogger, Types, Log, Config)
#
# USAGE:
#     >>> import traceline
#     >>> logger = traceline.get_logger()
#     >>> logger.log("Hello, world!", LogType.DEBUG)
#     >>> 
#     >>> # Or use the default singleton
#     >>> traceline.logger_instance.log("Direct logging", LogType.DEBUG)
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

# Core Logger
from .Logger import get_logger, LoggerBuilder

# Logger Runtime
from .AsyncLogger import AsyncLogger

# Type System
from .Types import LogType, Color, get_color

# Formatter
from .Log import log

# Configuration Loader
from .Config import get_config

# Public Interface
__all__ = [
    "get_logger",
    "LoggerBuilder",
    "AsyncLogger",
    "LogType",
    "Color",
    "get_color",
    "log",
    "get_config",
]

__version__ = "0.1.1"

logger_instance = get_logger()

# ========================================================= END OF FILE =========================================================
