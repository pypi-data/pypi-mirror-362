from typing import Any, Literal

import pytest

from lite_dist2.expections import LD2ModelTypeError
from lite_dist2.value_models.point import ScalarValue, VectorValue


@pytest.mark.parametrize(
    ("json_dict", "expected"),
    [
        (
            {"type": "scalar", "value_type": "bool", "value": True, "name": "some flag"},
            ScalarValue(type="scalar", value_type="bool", value=True, name="some flag"),
        ),
        (
            {"type": "scalar", "value_type": "int", "value": "f23", "name": "some int"},
            ScalarValue(type="scalar", value_type="int", value="f23", name="some int"),
        ),
        (
            {"type": "scalar", "value_type": "float", "value": "0x1.999999999999ap-4", "name": "some float"},
            ScalarValue(type="scalar", value_type="float", value="0x1.999999999999ap-4", name="some float"),
        ),
    ],
)
def test_scalar_value_deserialize(json_dict: dict[str, Any], expected: ScalarValue) -> None:
    actual = ScalarValue.model_validate(json_dict)
    assert actual == expected


@pytest.mark.parametrize(
    ("scalar_value", "expected"),
    [
        (ScalarValue(type="scalar", value_type="bool", value=True), True),
        (ScalarValue(type="scalar", value_type="int", value="f23"), 3875),
        (ScalarValue(type="scalar", value_type="float", value="0x1.999999999999ap-4"), 0.1),
    ],
)
def test_scalar_value_numerize(scalar_value: ScalarValue, expected: bool | float) -> None:
    actual = scalar_value.numerize()
    assert actual == expected


def test_scalar_value_numerize_value_type_error() -> None:
    scalar = ScalarValue(type="scalar", value_type="bool", value=True)
    # noinspection PyTypeChecker
    scalar.value_type = "invalid"
    with pytest.raises(LD2ModelTypeError, match=r"Unknown\stype:\s"):
        _ = scalar.numerize()


@pytest.mark.parametrize(
    ("raw_result_value", "value_type", "name", "expected"),
    [
        (True, "bool", "flag", ScalarValue(type="scalar", value_type="bool", value=True, name="flag")),
        (3875, "int", "num", ScalarValue(type="scalar", value_type="int", value="0xf23", name="num")),
        (0.1, "float", None, ScalarValue(type="scalar", value_type="float", value="0x1.999999999999ap-4")),
    ],
)
def test_scalar_value_create_from_numeric(
    raw_result_value: bool | float,
    value_type: Literal["bool", "int", "float"],
    name: str | None,
    expected: ScalarValue,
) -> None:
    actual = ScalarValue.create_from_numeric(raw_result_value, value_type, name)
    assert actual == expected


def test_scalar_value_create_from_numeric_value_type_error() -> None:
    with pytest.raises(LD2ModelTypeError, match=r"Unknown\stype:\s"):
        # noinspection PyTypeChecker
        _ = ScalarValue.create_from_numeric(raw_result_value=True, value_type="invalid")


@pytest.mark.parametrize(
    ("json_dict", "expected"),
    [
        (
            {"type": "vector", "value_type": "bool", "values": [True], "name": "some flag"},
            VectorValue(type="vector", value_type="bool", values=[True], name="some flag"),
        ),
        (
            {"type": "vector", "value_type": "int", "values": ["0xf23"], "name": "some int"},
            VectorValue(type="vector", value_type="int", values=["0xf23"], name="some int"),
        ),
        (
            {"type": "vector", "value_type": "float", "values": ["0x1.999999999999ap-4"], "name": "some float"},
            VectorValue(type="vector", value_type="float", values=["0x1.999999999999ap-4"], name="some float"),
        ),
    ],
)
def test_vector_value_deserialize(json_dict: dict[str, Any], expected: VectorValue) -> None:
    actual = VectorValue.model_validate(json_dict)
    assert actual == expected


@pytest.mark.parametrize(
    ("vector_value", "expected"),
    [
        (VectorValue(type="vector", value_type="bool", values=[True]), [True]),
        (VectorValue(type="vector", value_type="int", values=["f23"]), [3875]),
        (VectorValue(type="vector", value_type="float", values=["0x1.999999999999ap-4"]), [0.1]),
    ],
)
def test_vector_value_numerize(vector_value: VectorValue, expected: list[bool | int | float]) -> None:
    actual = vector_value.numerize()
    assert actual == expected


def test_vector_value_numerize_value_type_error() -> None:
    vector = VectorValue(type="vector", value_type="bool", values=[True])
    # noinspection PyTypeChecker
    vector.value_type = "invalid"
    with pytest.raises(LD2ModelTypeError, match=r"Unknown\stype:\s"):
        _ = vector.numerize()


@pytest.mark.parametrize(
    ("raw_result_value", "value_type", "name", "expected"),
    [
        ([True], "bool", "flag", VectorValue(type="vector", value_type="bool", values=[True], name="flag")),
        ([3875], "int", "num", VectorValue(type="vector", value_type="int", values=["0xf23"], name="num")),
        ([0.1], "float", None, VectorValue(type="vector", value_type="float", values=["0x1.999999999999ap-4"])),
    ],
)
def test_vector_value_create_from_numeric(
    raw_result_value: list[bool | int | float],
    value_type: Literal["bool", "int", "float"],
    name: str | None,
    expected: VectorValue,
) -> None:
    actual = VectorValue.create_from_numeric(raw_result_value, value_type, name)
    assert actual == expected


def test_vector_value_create_from_numeric_value_type_error() -> None:
    with pytest.raises(LD2ModelTypeError, match=r"Unknown\stype:\s"):
        # noinspection PyTypeChecker
        _ = VectorValue.create_from_numeric(raw_result_value=[True], value_type="invalid")
