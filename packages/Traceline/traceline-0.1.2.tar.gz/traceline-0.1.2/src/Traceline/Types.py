# ──────────────────────────────────────────────────────────────────────────────────────
#                               TRACELINE LOGGING TYPES
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : Types.py
#     Module Name    : Traceline Logging Types
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.5
#
# FILE DESCRIPTION:
#     Core type system for Traceline Logger providing enumerated log levels,
#     ANSI color codes, and type-safe utility functions. Implements Result-based
#     error handling for all type conversions and validations.
#
# PROGRAM DESCRIPTION:
#     Primary Functions:
#       • LogType enum with hierarchical priority system (DEBUG to CRITICAL)
#       • Color enum with ANSI escape codes for terminal output
#       • Type-safe string-to-LogType conversion with error handling
#       • Color mapping system linking log types to display colors
#       • Priority comparison and validation methods
#       • Type aliases for clean API interfaces
#
# SECURITY CONSIDERATIONS:
#     • Input validation prevents invalid enum construction
#     • Result pattern eliminates exception-based error handling
#     • ANSI codes are predefined constants preventing injection
#     • Type system enforces compile-time safety where possible
#
# REQUIREMENTS:
#     Python Version : 3.11+
#     Dependencies   : enum, typing, returns
#
# USAGE:
#     >>> from traceline import LogType, Color, get_color
#     >>> 
#     >>> # LogType creation and validation
#     >>> log_type = LogType.from_str("INFO").unwrap()
#     >>> print(log_type.priority().unwrap())  # 1
#     >>> 
#     >>> # Priority comparisons
#     >>> LogType.ERROR.is_louder(LogType.INFO)  # True
#     >>> 
#     >>> # Color mapping
#     >>> color = get_color(LogType.ERROR).unwrap()
#     >>> print(f"{color.value}Error message{Color.RESET.value}")
#     >>> 
#     >>> # All available log types
#     >>> print(LogType.all_names())  # ['DEBUG', 'INFO', ...]
#
# ERROR HANDLING:
#     - Enum validation handled by Python enum module
#     - Type safety enforced through enumeration and Result pattern
#     - Result pattern implementation for safe error handling
#     - ValueError exceptions wrapped in Failure results for invalid inputs
#     - Color mapping errors handled through get_color() function
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
# NOTES:
#     1. Maintains strict error handling with Result pattern
#     2. LogType priority scale: DEBUG(0) < INFO/MESSAGE(1) < SUCCESS(2) < WARNING(3) < ERROR(4) < CRITICAL(5) < QUIET(6)
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

from enum import Enum, unique
from typing import Final, Mapping, TypeAlias, Literal
from returns.result import Result, Failure, Success

# ANSI Color Enum
@unique
class Color(Enum):
    RED     = "\x1b[31m"
    GREEN   = "\x1b[32m"
    YELLOW  = "\x1b[33m"
    BLUE    = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN    = "\x1b[36m"
    WHITE   = "\x1b[37m"
    GRAY    = "\x1b[90m"
    RESET   = "\x1b[0m"

# LogType Enum
class LogType(Enum):
    DEBUG       = 0
    INFO        = 1
    MESSAGE     = 1
    SUCCESS     = 2
    WARNING     = 3
    ERROR       = 4
    CRITICAL    = 5
    QUIET       = 6

    def priority(self) -> Result[int, ValueError]:
        return Success(self.value)
    
    def is_louder(self, other: 'LogType') -> bool:
        return self.value >= other.value
    
    @staticmethod
    def from_str(name: str) -> Result['LogType', ValueError]:
        try:
            normalized = name.strip().upper()
            return Success(LogType[normalized])
        except KeyError:
            return Failure(ValueError(f"Unrecognized LogType: '{name}'"))
        
    @staticmethod
    def all_names() -> list[str]:
        return [lt.name for lt in LogType]
    
# Mapping from LogType to Color
LOGTYPE_COLOR_MAPPING: Final[Mapping[LogType, Color]] = {
    LogType.DEBUG:      Color.BLUE,
    LogType.ERROR:      Color.RED,
    LogType.WARNING:    Color.YELLOW,
    LogType.INFO:       Color.CYAN,
    LogType.MESSAGE:    Color.CYAN,
    LogType.CRITICAL:   Color.MAGENTA,
    LogType.SUCCESS:    Color.GREEN,
    LogType.QUIET:      Color.GRAY
}

def get_color(logtype: LogType) -> Result[Color, ValueError]:
    color = LOGTYPE_COLOR_MAPPING.get(logtype)
    return Success(color) if color else Failure(ValueError(f"No color mapping for LogType: {logtype.name}"))

# Type Aliases for Clean Interfaces
LogTypeName: TypeAlias = Literal[
    "DEBUG", "INFO", "MESSAGE", "SUCCESS", "WARNING", "ERROR", "CRITICAL", "QUIET"
]

AnsiCode: TypeAlias = str

# ========================================================= END OF FILE =========================================================
