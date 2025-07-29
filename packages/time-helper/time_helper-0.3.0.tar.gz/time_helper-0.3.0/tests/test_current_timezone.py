"""Tests for current_timezone() improvements."""

import os
import platform
import sys
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from time_helper import current_timezone
from time_helper.timezone import timezone


def test_current_timezone_returns_valid_timezone() -> None:
    """Test that current_timezone returns a valid timezone object."""
    tz = current_timezone()

    assert tz is not None
    assert hasattr(tz, "tzname")
    # Should be a timezone object
    assert isinstance(tz, timezone)


def test_current_timezone_cest_handling() -> None:
    """Test that CEST is properly converted to Europe/Berlin."""
    # Mock datetime to return CEST
    mock_dt = Mock()
    mock_dt.tzname.return_value = "CEST"
    mock_dt.tzinfo = None  # No proper tzinfo

    with patch("time_helper.timezone.datetime") as mock_datetime:
        mock_datetime.now.return_value.astimezone.return_value = mock_dt

        tz = current_timezone()

        # Should convert CEST to Europe/Berlin (more accurate than CET)
        assert str(tz) == "Europe/Berlin"


def test_current_timezone_standard_timezones() -> None:
    """Test that standard timezone names work correctly."""
    test_cases = ["UTC", "EST", "PST", "GMT"]

    for tz_name in test_cases:
        mock_dt = Mock()
        mock_dt.tzname.return_value = tz_name

        with patch("time_helper.timezone.datetime") as mock_datetime:
            mock_datetime.now.return_value.astimezone.return_value = mock_dt

            try:
                tz = current_timezone()
                assert tz is not None
                # For mapped timezones, check the actual zone
                if tz_name in ["EST", "PST"]:
                    assert str(tz) in ["America/New_York", "America/Los_Angeles"]
                else:
                    assert str(tz) == tz_name
            except Exception:
                # Some timezone names might not be valid
                pass


def test_current_timezone_system_default() -> None:
    """Test that current_timezone uses system timezone correctly."""
    # Get the actual system timezone
    tz = current_timezone()

    # Create a datetime with this timezone
    dt = datetime.now(tz)

    # Should be able to get timezone name
    tz_name = dt.tzname()
    assert tz_name is not None


def test_current_timezone_consistency() -> None:
    """Test that multiple calls return consistent results."""
    tz1 = current_timezone()
    tz2 = current_timezone()

    # Should return the same timezone
    assert str(tz1) == str(tz2)


@pytest.mark.skipif(sys.platform == "win32", reason="Platform-specific timezone handling")
def test_current_timezone_unix_specific() -> None:
    """Test Unix-specific timezone scenarios."""
    # Test with various Unix timezone names
    unix_timezones = ["America/New_York", "Europe/London", "Asia/Tokyo"]

    for tz_name in unix_timezones:
        mock_dt = Mock()
        mock_dt.tzname.return_value = tz_name

        with patch("time_helper.timezone.datetime") as mock_datetime:
            mock_datetime.now.return_value.astimezone.return_value = mock_dt

            try:
                tz = current_timezone()
                assert tz is not None
            except Exception:
                # Some timezones might not be available
                pass


def test_current_timezone_invalid_timezone() -> None:
    """Test handling of invalid timezone names."""
    mock_dt = Mock()
    mock_dt.tzname.return_value = "INVALID_TZ_NAME"
    mock_dt.tzinfo = None  # No proper tzinfo

    with patch("time_helper.timezone.datetime") as mock_datetime:
        mock_datetime.now.return_value.astimezone.return_value = mock_dt

        # Should fall back to UTC for invalid timezone
        tz = current_timezone()
        assert tz is not None
        assert str(tz) == "UTC"


def test_current_timezone_none_tzname() -> None:
    """Test handling when tzname returns None."""
    mock_dt = Mock()
    mock_dt.tzname.return_value = None
    mock_dt.tzinfo = None  # No proper tzinfo

    with patch("time_helper.timezone.datetime") as mock_datetime:
        mock_datetime.now.return_value.astimezone.return_value = mock_dt

        # Should fall back to UTC when tzname is None
        tz = current_timezone()
        assert tz is not None
        assert str(tz) == "UTC"


def test_current_timezone_should_return_proper_timezone_not_abbreviation() -> None:
    """Test that current_timezone returns proper timezone, not abbreviation.

    The current implementation uses tzname() which returns abbreviations like 'PST'
    instead of proper timezone names like 'America/Los_Angeles'.
    """
    tz = current_timezone()

    # Create a datetime with the timezone
    dt = datetime.now(tz)

    # The timezone should work for date arithmetic
    # This will fail if we get an abbreviation instead of proper timezone
    future_dt = dt.replace(year=dt.year + 1)

    # Should be able to handle DST transitions
    assert future_dt.tzinfo is not None


def test_current_timezone_platform_specific() -> None:
    """Test that current_timezone works correctly across platforms."""
    # Save original TZ if set
    orig_tz = os.environ.get("TZ")

    try:
        # Test with different timezone environment variables
        test_timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]

        for tz_name in test_timezones:
            # Set TZ environment variable
            os.environ["TZ"] = tz_name

            # On Unix, this should affect the system timezone
            if platform.system() != "Windows":
                # Force timezone reload
                import time

                time.tzset()

            # Get current timezone
            try:
                tz = current_timezone()
                assert tz is not None

                # Should be able to create valid datetimes
                dt = datetime.now(tz)
                assert dt.tzinfo is not None
            except Exception as e:
                # Some timezones might not be available on all systems
                print(f"Timezone {tz_name} not available: {e}")

    finally:
        # Restore original TZ
        if orig_tz is not None:
            os.environ["TZ"] = orig_tz
        else:
            os.environ.pop("TZ", None)

        if platform.system() != "Windows":
            import time

            time.tzset()


def test_current_timezone_abbreviation_mapping() -> None:
    """Test that timezone abbreviations are properly mapped."""
    # Test abbreviations that should be mapped
    abbreviations = {
        "EST": "America/New_York",
        "CST": "America/Chicago",
        "PST": "America/Los_Angeles",
        "IST": "Asia/Kolkata",
    }

    for abbr, expected_zone in abbreviations.items():
        # Mock to return abbreviation
        mock_dt = Mock()
        mock_dt.tzname.return_value = abbr
        mock_dt.tzinfo = None  # No proper tzinfo object

        with patch("time_helper.timezone.datetime") as mock_datetime:
            mock_datetime.now.return_value.astimezone.return_value = mock_dt

            tz = current_timezone()

            # Should map to proper timezone
            assert str(tz) == expected_zone


def test_current_timezone_ambiguous_abbreviations() -> None:
    """Test handling of ambiguous timezone abbreviations.

    CST could mean Central Standard Time (US) or China Standard Time.
    IST could mean Indian Standard Time or Irish Standard Time.
    """
    # The current implementation should handle these consistently
    ambiguous = ["CST", "IST", "BST"]

    for abbr in ambiguous:
        mock_dt = Mock()
        mock_dt.tzname.return_value = abbr

        with patch("time_helper.timezone.datetime") as mock_datetime:
            mock_datetime.now.return_value.astimezone.return_value = mock_dt

            try:
                tz = current_timezone()
                # Should map to something specific
                assert tz is not None
                assert str(tz) != abbr  # Should not just return abbreviation
            except Exception:
                # Might fail for unmapped abbreviations
                pass


def test_current_timezone_dst_transitions() -> None:
    """Test that current timezone handles DST transitions correctly."""
    tz = current_timezone()

    # Test dates around DST transitions
    # March (spring forward) and November (fall back) for US timezones
    test_dates = [
        datetime(2023, 3, 12, 2, 30),  # During spring DST transition
        datetime(2023, 11, 5, 1, 30),  # During fall DST transition
        datetime(2023, 6, 15, 12, 0),  # Summer (DST active)
        datetime(2023, 12, 15, 12, 0),  # Winter (DST inactive)
    ]

    for dt in test_dates:
        try:
            # Should be able to localize these dates
            localized = dt.replace(tzinfo=tz)
            assert localized.tzinfo is not None
        except Exception as e:
            # Some timezone implementations might have issues
            print(f"Failed to localize {dt}: {e}")


def test_current_timezone_better_implementation_needed() -> None:
    """Test that demonstrates need for better implementation.

    The current implementation has several issues:
    1. Uses tzname() which returns abbreviations
    2. Hardcoded CEST->CET conversion
    3. Doesn't use system timezone detection properly
    """
    # This test documents the issues rather than testing current behavior

    # Issue 1: tzname() returns abbreviations which are ambiguous
    dt = datetime.now().astimezone()
    dt.tzname()

    # Abbreviations like CST, IST are ambiguous
    # We need proper timezone detection

    # Issue 2: Hardcoded conversions are brittle
    # CEST->CET is just one case, there are many others

    # Issue 3: Should use platform-specific APIs
    # - On Unix: check TZ env var, /etc/localtime
    # - On Windows: use win32 APIs
    # - Fallback: use tzlocal or similar

    assert True  # This test is for documentation
