# ──────────────────────────────────────────────────────────────────────────────────────
#                             TRACELINE LOGGING TYPE TESTS
#                              (Comprehensive Unit Tests)
# ──────────────────────────────────────────────────────────────────────────────────────
#
# FILE IDENTIFICATION:
#     File Name      : test_Types.py
#     Module Name    : Traceline Logging Type Tests
#     Project ID     : HYRA-0.traceline
#     File Version   : 0.1.0
#
# SYSTEM INTEGRATION:
#     Part of        : HYRA‑0 – Zero‑Database Mathematical & Physical Reasoning Engine
#     Subsystem      : Traceline Logging Core
#
# MAINTAINABILITY:
#     Author         : Michael Tang
#     Organization   : BioNautica Research Initiative
#     Contact        : michaeltang@bionautica.org
#     Created        : 2025‑07‑10
#     Last Updated   : 2025‑07‑10
#     Repository     : https://projects.bionautica.org/hyra-zero/traceline
#     License        : Apache License v2.0
#
# © 2025 Michael Tang / BioNautica Research Initiative. All rights reserved.
# ──────────────────────────────────────────────────────────────────────────────────────

from enum import Enum

from returns.result import Failure

from Traceline.Types import LogType, Color, get_color

# Unit Tests --------------------------------------------------------------------------------------------------------------------

def test_logtype_priority_and_comparison() -> None:
    assert LogType.DEBUG.priority().unwrap() == 0
    assert LogType.ERROR.priority().unwrap() == 4
    assert LogType.ERROR.is_louder(LogType.INFO) is True
    assert LogType.INFO.is_louder(LogType.CRITICAL) is False

def test_logtype_from_str_success_and_failure() -> None:
    ok = LogType.from_str("  info ").unwrap()
    assert ok is LogType.INFO

    bad = LogType.from_str("invalid")
    assert isinstance(bad, Failure)
    assert isinstance(bad.failure(), ValueError)
    assert "Unrecognized" in str(bad.failure())

def test_logtype_all_names_cocmpleteness() -> None:
    names = LogType.all_names()
    assert set(names) == {m.name for m in LogType}
    assert names[0] == "DEBUG"

def test_get_color_failure_branch_with_fake_enum() -> None:
    class FakeLogType(Enum):
        UNKNOWN = 999

    # Type ignore because we're intentionally testing with wrong type
    fail = get_color(FakeLogType.UNKNOWN)  # type: ignore[arg-type]
    assert isinstance(fail, Failure)
    assert isinstance(fail.failure(), ValueError)
    assert "No color mapping" in str(fail.failure())

def test_get_enum_values_are_ansi_sequences() -> None:
    for color in Color:
        assert color.value.startswith("\033")

# ========================================================= END OF FILE =========================================================
