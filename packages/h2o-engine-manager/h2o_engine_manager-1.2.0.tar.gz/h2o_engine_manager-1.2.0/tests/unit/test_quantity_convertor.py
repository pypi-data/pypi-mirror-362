import pytest

from h2o_engine_manager.clients.convert.quantity_convertor import *


@pytest.mark.parametrize("quantity", ["5GiB", "5 Gi", "5.8Gi"])
def test_invalid_quantity(quantity):
    with pytest.raises(ValueError):
        quantity_to_number(quantity)


@pytest.mark.parametrize(
    "quantity,expected",
    [
        ("5Gi", 5 << 30),
        ("5G", 5 * (10**9)),
        ("5Mi", 5 << 20),
        ("5M", 5 * (10**6)),
        ("5", 5),
    ],
)
def test_quantity_to_number(quantity, expected):
    assert quantity_to_number(quantity) == expected


@pytest.mark.parametrize(
    "number,expected",
    [
        (5 << 30, "5Gi"),
        (5 * (10**9), "5G"),
        (5 << 20, "5Mi"),
        (5 * (10**6), "5M"),
        (5, "5"),
        (1024, "1Ki"),
        (1000, "1k"),
        (1025, "1025"),
        (2048, "2Ki"),
        (1024 * 1024 * 1024, "1Gi"),
    ],
)
def test_number_to_quantity(number, expected):
    assert number_to_quantity(number) == expected
