import pytest

from lite_dist2.expections import LD2UndefinedError
from lite_dist2.type_definitions import PortableValueType, PrimitiveValueType
from lite_dist2.value_models.base_space import FlattenSegment
from lite_dist2.value_models.jagged_space import ParameterJaggedSpace, ParameterJaggedSpaceModel
from lite_dist2.value_models.line_segment import DummyLineSegment, LineSegmentModel


def test_parameter_jagged_space_hash() -> None:
    space = ParameterJaggedSpace(
        parameters=[(1,)],
        ambient_indices=[(1,)],
        axes_info=[
            DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
        ],
    )
    _ = hash(space)


@pytest.mark.parametrize(
    ("space", "expected"),
    [
        pytest.param(
            ParameterJaggedSpace(
                parameters=[(1,)],
                ambient_indices=[(1,)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
                ],
            ),
            (1,),
            id="1D",
        ),
        pytest.param(
            ParameterJaggedSpace(
                parameters=[(1,), (2,)],
                ambient_indices=[(1,), (2,)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
                ],
            ),
            (1,),
            id="1D(parameter affect nothing)",
        ),
        pytest.param(
            ParameterJaggedSpace(
                parameters=[(False, 0, 0)],
                ambient_indices=[(0, 0, 0)],
                axes_info=[
                    DummyLineSegment(name="tf", type="bool", step=1, ambient_size=2),
                    DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
                    DummyLineSegment(name="y", type="int", step=1, ambient_size=70),
                ],
            ),
            (7000, 70, 1),
            id="Multi D",
        ),
    ],
)
def test_parameter_jagged_space_lower_element_num_by_dim(
    space: ParameterJaggedSpace,
    expected: tuple[int, ...],
) -> None:
    actual = space.lower_element_num_by_dim()
    assert actual == expected


@pytest.mark.parametrize(
    ("space", "expected"),
    [
        pytest.param(
            ParameterJaggedSpace(
                parameters=[(0,), (1,)],
                ambient_indices=[(0,), (1,)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
                ],
            ),
            [
                FlattenSegment(start=0, size=1),
                FlattenSegment(start=1, size=1),
            ],
            id="1D",
        ),
        pytest.param(
            ParameterJaggedSpace(
                parameters=[(78, 1), (1, 78)],
                ambient_indices=[(78, 1), (1, 78)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", step=1, ambient_size=100),
                    DummyLineSegment(name="y", type="int", step=1, ambient_size=100),
                ],
            ),
            [
                FlattenSegment(start=7801, size=1),
                FlattenSegment(start=178, size=1),
            ],
            id="2D",
        ),
    ],
)
def test_parameter_jagged_space_get_flatten_ambient_start_and_size_list(
    space: ParameterJaggedSpace,
    expected: list[FlattenSegment],
) -> None:
    actual = space.get_flatten_ambient_start_and_size_list()
    assert actual == expected


@pytest.mark.parametrize(
    "model",
    [
        pytest.param(
            ParameterJaggedSpaceModel(
                type="jagged",
                parameters=[("0x4e", "0x1"), ("0x1", "0x4e")],
                ambient_indices=[("0x4e", "0x1"), ("0x1", "0x4e")],
                axes_info=[
                    LineSegmentModel(
                        name="x",
                        type="int",
                        size="0x1",
                        step="0x1",
                        start="0x0",
                        ambient_index="0x0",
                        ambient_size="0x64",
                        is_dummy=True,
                    ),
                ],
            ),
        ),
    ],
)
def test_parameter_jagged_space_to_model_from_model(model: ParameterJaggedSpaceModel) -> None:
    space = ParameterJaggedSpace.from_model(model)
    reconstructed = space.to_model()
    assert model == reconstructed


@pytest.mark.parametrize(
    ("primitive", "expected"),
    [
        pytest.param(False, False, id="bool"),
        pytest.param(100, "0x64", id="int"),
        pytest.param(0.25, "0x1.0000000000000p-2", id="float"),
    ],
)
def test_parameter_jagged_space_primitive_to_portable(
    primitive: PrimitiveValueType,
    expected: PortableValueType,
) -> None:
    actual = ParameterJaggedSpace._primitive_to_portable(primitive)
    assert actual == expected


def test_parameter_jagged_space_primitive_to_portable_raise_undefined_type() -> None:
    with pytest.raises(LD2UndefinedError):
        # noinspection PyTypeChecker
        ParameterJaggedSpace._primitive_to_portable([])


@pytest.mark.parametrize(
    ("portable", "expected"),
    [
        pytest.param(False, False, id="bool"),
        pytest.param("0x64", 100, id="int"),
        pytest.param("0x1.0000000000000p-2", 0.25, id="float"),
    ],
)
def test_parameter_jagged_space_portable_to_primitive(
    portable: PortableValueType,
    expected: PrimitiveValueType,
) -> None:
    actual = ParameterJaggedSpace._portable_to_primitive(portable)
    assert actual == expected


def test_parameter_jagged_space_portable_to_primitive_raise_undefined_type() -> None:
    with pytest.raises(LD2UndefinedError):
        # noinspection PyTypeChecker
        ParameterJaggedSpace._portable_to_primitive([])
