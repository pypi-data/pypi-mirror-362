import pytest

from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.type_definitions import PortableValueType
from lite_dist2.value_models.point import ScalarValue, VectorValue


@pytest.mark.parametrize(
    ("mapping", "expected"),
    [
        pytest.param(
            Mapping(
                params=(
                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                ),
                result=ScalarValue(type="scalar", value_type="int", value="0x2"),
            ),
            ("0x0", "0x1", "0x2"),
            id="scalar",
        ),
        pytest.param(
            Mapping(
                params=(
                    ScalarValue(type="scalar", value_type="bool", value=True, name="x"),
                    ScalarValue(type="scalar", value_type="float", value="0x1.0000000000000p+0", name="y"),
                ),
                result=VectorValue(type="vector", value_type="int", values=["0x2", "0x3"]),
            ),
            (True, "0x1.0000000000000p+0", "0x2", "0x3"),
            id="scalar",
        ),
    ],
)
def test_mapping_to_tuple(mapping: Mapping, expected: tuple[PortableValueType]) -> None:
    actual = mapping.to_tuple()
    assert actual == expected
