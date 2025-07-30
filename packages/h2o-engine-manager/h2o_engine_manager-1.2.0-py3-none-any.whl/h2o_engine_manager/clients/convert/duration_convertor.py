import re
from typing import Optional

suffix_values = {"d": 86400, "h": 3600, "m": 60, "s": 1}


def optional_duration_to_seconds(duration: Optional[str]) -> Optional[str]:
    if duration is None:
        return None
    return duration_to_seconds(duration)


def duration_to_seconds(duration: str) -> str:
    """
    Converts duration specified in seconds, minutes, hours or days into a durating specified in seconds.
    [duration] = [number][suffix]
    [suffix] = s | m | h | d

    Args:
        duration: string representing duration in format of number with a `s` suffix. Example `3600s`.

    Returns:
        string representing duration in seconds with a `s` suffix.

    Raises:
        ValueError: Invalid duration value passed.

    Examples:
        - "1s" -> "1s"
        - "1m" -> "60s"
        - "1h" -> "3600s"
        - "1d" -> "86400s"
        - "1w" -> "ValueError"
        - "60" -> "ValueError"
    """
    duration_regex = re.compile("^[0-9]+(s|m|h|d)$")
    if duration_regex.match(duration) is None:
        raise ValueError(f"invalid duration format: {duration}")

    num_regex = re.compile("^[0-9]+")
    match = num_regex.search(duration)
    if match is None:
        # This should never happen because duration_regex already covers this.
        raise Exception("number not found in duration expression")

    num = int(match.group())
    suffix = num_regex.split(duration)[1]

    multiplier = 1

    if suffix:
        value = suffix_values.get(suffix)
        if value is None:
            raise Exception(f"unsupported duration suffix: {suffix}")
        multiplier = value

    return f"{num * multiplier}s"


def optional_seconds_to_duration(seconds: Optional[str]) -> Optional[str]:
    if not seconds:
        return None
    return seconds_to_duration(seconds)


def seconds_to_duration(seconds: str) -> str:
    """
    Converts seconds into a human-readable duration string. The highest possible duration unit will be
    applied.

    Args:
        seconds: number of seconds followed with a `s` suffix. Decimal values will be rounded down.

    Returns:
        string representing duration in highest possible unit available (up to `d` representing days).

    Examples:
        "1s" -> "1s"
        "1.9s" -> "1s"
        "60s" -> "1m"
        "61s" -> "61s"
        "3600s" -> "1h"
        "3601s" -> "3601s"
    """
    duration_regex = re.compile("^[0-9]+[.]?[0-9]*s$")
    if duration_regex.match(seconds) is None:
        raise ValueError(f"invalid duration format: {seconds}")

    num = int(float(seconds.rstrip("s")))

    # Special case for zero value
    if num == 0:
        return "0s"

    for suffix, multiplier in suffix_values.items():
        if num % multiplier == 0:
            return f"{int(num / multiplier)}{suffix}"

    return f"{num}s"
