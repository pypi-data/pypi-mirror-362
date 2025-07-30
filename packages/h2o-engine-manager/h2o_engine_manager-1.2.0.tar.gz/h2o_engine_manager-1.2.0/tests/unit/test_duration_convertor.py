import pytest

from h2o_engine_manager.clients.convert.duration_convertor import *


@pytest.mark.parametrize("duration", ["10", "-10s", "1w", "1sec", "1min"])
def test_invalid_duration(duration):
    with pytest.raises(ValueError):
        duration_to_seconds(duration)


@pytest.mark.parametrize(
    "duration,expected",
    [("1s", "1s"), ("1m", "60s"), ("12h", "43200s"), ("2d", "172800s")],
)
def test_duration_to_seconds(duration, expected):
    assert duration_to_seconds(duration) == expected


@pytest.mark.parametrize(
    "seconds,expected", [("1s", "1s"), ("2.99s", "2s"), ("60s", "1m"), ("61s", "61s"), ("43200s", "12h")]
)
def test_seconds_to_duration(seconds, expected):
    assert seconds_to_duration(seconds) == expected
