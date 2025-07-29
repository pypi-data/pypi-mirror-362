from typing import Literal

import pytest

from lite_dist2 import common
from lite_dist2.type_definitions import PortableValueType, PrimitiveValueType


@pytest.mark.parametrize(
    ("hex_str", "expected"),
    [
        ("0x0", 0),
        ("0x01", 1),
        ("0xa", 10),
        ("0xa54f", 42319),
        ("-0x1", -1),
    ],
)
def test_hex2int(hex_str: str, expected: int) -> None:
    assert common.hex2int(hex_str) == expected


@pytest.mark.parametrize(
    ("int_val", "expected"),
    [
        (0, "0x0"),
        (10, "0xa"),
        (42319, "0xa54f"),
        (-1, "-0x1"),
    ],
)
def test_int2hex(int_val: int, expected: str) -> None:
    assert common.int2hex(int_val) == expected


@pytest.mark.parametrize(
    ("hex_str", "expected"),
    [
        ("0x0.0p+0", 0.0),
        ("-0x0.0p+0", -0.0),
        ("0x1.999999999999ap-4", 0.1),
    ],
)
def test_hex2float(hex_str: str, expected: float) -> None:
    assert common.hex2float(hex_str) == expected


@pytest.mark.parametrize(
    ("float_val", "expected"),
    [
        (0.0, "0x0.0p+0"),
        (-0.0, "-0x0.0p+0"),
        (0.1, "0x1.999999999999ap-4"),
    ],
)
def test_float2hex(float_val: float, expected: str) -> None:
    assert common.float2hex(float_val) == expected


@pytest.mark.parametrize(
    ("type_name", "value", "expected"),
    [
        ("bool", False, False),
        ("int", "0x2", 2),
        ("float", "0x1.999999999999ap-4", 0.1),
    ],
)
def test_numerize(
    type_name: Literal["bool", "int", "float"],
    value: PortableValueType,
    expected: PrimitiveValueType,
) -> None:
    actual = common.numerize(type_name, value)
    assert actual == expected


@pytest.mark.parametrize(
    ("type_name", "value", "expected"),
    [
        ("bool", False, False),
        ("int", 2, "0x2"),
        ("float", 0.1, "0x1.999999999999ap-4"),
    ],
)
def test_portablize(
    type_name: Literal["bool", "int", "float"],
    value: PrimitiveValueType,
    expected: PortableValueType,
) -> None:
    actual = common.portablize(type_name, value)
    assert actual == expected
