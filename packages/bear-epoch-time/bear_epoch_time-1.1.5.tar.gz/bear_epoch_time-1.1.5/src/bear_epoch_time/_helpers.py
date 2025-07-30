from datetime import timedelta
from typing import Any

try:
    from warnings import deprecated  # type: ignore[import] Python 3.13+
except ImportError:

    class deprecated:
        """A decorator to mark functions as deprecated."""

        def __init__(self, message: str):
            self.message = message

        def __call__(self, func):
            def wrapper(*args, **kwargs):
                print(f"Warning: {self.message}")
                return func(*args, **kwargs)

            return wrapper


from bear_epoch_time.time_converter import TimeConverter


@deprecated("use TimeConverter.parse_to_seconds")
def convert_to_seconds(time_str: str) -> float:
    """Convert a time string to seconds. (Deprecated: use TimeConverter.parse_to_seconds)"""
    return TimeConverter.parse_to_seconds(time_str)


@deprecated("use TimeConverter.parse_to_milliseconds")
def convert_to_milliseconds(time_str: str) -> float:
    """Convert a time string to milliseconds. (Deprecated: use TimeConverter.parse_to_milliseconds)"""
    return TimeConverter.parse_to_milliseconds(time_str)


@deprecated("use TimeConverter.format_seconds")
def seconds_to_time(seconds: float, show_subseconds: bool = True) -> str:
    """Convert seconds to time string. (Deprecated: use TimeConverter.format_seconds)"""
    return TimeConverter.format_seconds(seconds, show_subseconds)


@deprecated("use TimeConverter.format_milliseconds")
def milliseconds_to_time(milliseconds: float) -> str:
    """Convert milliseconds to time string. (Deprecated: use TimeConverter.format_milliseconds)"""
    return TimeConverter.format_milliseconds(milliseconds)


@deprecated("use TimeConverter.to_timedelta")
def seconds_to_timedelta(seconds: float) -> timedelta:
    """Convert seconds to timedelta. (Deprecated: use TimeConverter.to_timedelta)"""
    return TimeConverter.to_timedelta(seconds)


@deprecated("use TimeConverter.from_timedelta")
def timedelta_to_seconds(td: timedelta | Any) -> float:
    """Convert timedelta to seconds. (Deprecated: use TimeConverter.from_timedelta)"""
    return TimeConverter.from_timedelta(td)


if __name__ == "__main__":
    # DEPRECATED: Use TimeConverter.parse_to_seconds
    print(convert_to_seconds("2h 30m 15s"))
    print(convert_to_milliseconds("1d 2h 3m 4s 500ms"))
    print(seconds_to_time(3661.5))
    print(milliseconds_to_time(1234567))
    print(seconds_to_timedelta(3600))
    print(timedelta_to_seconds(timedelta(days=1, hours=2, minutes=3)))
