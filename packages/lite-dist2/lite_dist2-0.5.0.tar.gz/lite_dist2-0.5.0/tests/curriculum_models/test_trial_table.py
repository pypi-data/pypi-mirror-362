from datetime import timedelta

import pytest
from pytest_mock import MockFixture

from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.curriculum_models.trial import Trial, TrialModel, TrialStatus
from lite_dist2.curriculum_models.trial_table import TrialTable, TrialTableModel
from lite_dist2.expections import LD2ParameterError
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.base_space import FlattenSegment
from lite_dist2.value_models.jagged_space import ParameterJaggedSpace
from lite_dist2.value_models.line_segment import DummyLineSegment, LineSegmentModel, ParameterRangeInt
from lite_dist2.value_models.point import ScalarValue
from tests.const import DT

_DUMMY_PARAMETER_SPACE = ParameterAlignedSpace(
    axes=[
        ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
        ParameterRangeInt(name="y", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
    ],
    check_lower_filling=True,
)


@pytest.mark.parametrize(
    ("table", "total_num", "expected"),
    [
        pytest.param(
            TrialTable(
                trials=[],  # ここでは使わないので空
                aggregated_parameter_space=None,
            ),
            100,
            FlattenSegment(0, None),
            id="Empty (None aps)",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={-1: [], 0: []},
            ),
            100,
            FlattenSegment(0, None),
            id="Empty",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    0: [],
                },
            ),
            10,
            FlattenSegment(10, 0),
            id="Universal 1D",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=None,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            None,
            FlattenSegment(10, None),
            id="Infinite 1D",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=50,
                                    ambient_size=100,
                                    start=50,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            10,
            FlattenSegment(10, 40),
            id="Segmented 1D",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=None,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=10,
                                    ambient_index=50,
                                    ambient_size=None,
                                    start=50,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            None,
            FlattenSegment(10, 40),
            id="Infinite segmented 1D",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    0: [],
                    1: [],
                },
            ),
            100,
            FlattenSegment(100, 0),
            id="Universal 2D",
        ),
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=10,
                                    start=1,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=5,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            100,
            FlattenSegment(5, 5),
            id="Segmented 2D",
        ),
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[
                                (1, 0),
                                (1, 1),
                                (1, 2),
                                (1, 3),
                                (1, 4),
                                (1, 5),
                                (1, 6),
                                (1, 7),
                                (1, 8),
                                (1, 9),
                            ],
                            ambient_indices=[
                                (1, 0),
                                (1, 1),
                                (1, 2),
                                (1, 3),
                                (1, 4),
                                (1, 5),
                                (1, 6),
                                (1, 7),
                                (1, 8),
                                (1, 9),
                            ],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=10, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=10, step=1),
                            ],
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xa", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xb", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xc", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xd", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xe", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x5", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xf", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x6", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x10", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x7", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x11", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x8", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x12", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x9", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x13", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[
                                (0, 0),
                                (0, 1),
                                (0, 2),
                                (0, 3),
                                (0, 4),
                            ],
                            ambient_indices=[
                                (0, 0),
                                (0, 1),
                                (0, 2),
                                (0, 3),
                                (0, 4),
                            ],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=10, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=10, step=1),
                            ],
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x1", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x2", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x3", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x4", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[
                                (0, 5),
                                (0, 6),
                                (0, 7),
                                (0, 8),
                                (0, 9),
                            ],
                            ambient_indices=[
                                (0, 5),
                                (0, 6),
                                (0, 7),
                                (0, 8),
                                (0, 9),
                            ],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=10, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=10, step=1),
                            ],
                        ),
                        trial_status=TrialStatus.running,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=10,
                                    start=1,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=5,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            100,
            FlattenSegment(20, None),
            id="Infinite jagged running 2D",
        ),
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=1,
                                    ambient_index=1,
                                    ambient_size=10,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    step=1,
                                    size=10,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xa", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xb", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xc", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xd", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xe", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x5", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0xf", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x6", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x10", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x7", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x11", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x8", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x12", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x9", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x13", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    step=1,
                                    size=5,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x1", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x2", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x3", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x4", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    step=1,
                                    size=5,
                                    start=5,
                                    ambient_index=5,
                                    ambient_size=10,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        trial_status=TrialStatus.running,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=10,
                                    start=1,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=10,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=5,
                                    ambient_index=0,
                                    ambient_size=10,
                                    start=0,
                                    step=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            100,
            FlattenSegment(20, None),
            id="Infinite aligned running 2D",
        ),
    ],
)
def test_trial_table_find_least_division(
    table: TrialTable,
    total_num: int,
    expected: FlattenSegment,
) -> None:
    actual = table.find_least_division(total_num)
    assert actual == expected


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(
            TrialTable(
                trials=[],
                aggregated_parameter_space=None,  # ここでは使わないので None
            ),
            0,
            id="Empty",
        ),
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    step=1,
                                    size=1,
                                    start=0,
                                    ambient_index=0,
                                    ambient_size=10,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        trial_status=TrialStatus.running,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                    ),
                ],
                aggregated_parameter_space=None,
            ),
            1,
            id="count only done aligned",
        ),
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[
                                (0, 3),
                                (0, 4),
                            ],
                            ambient_indices=[
                                (0, 3),
                                (0, 4),
                            ],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=10, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=10, step=1),
                            ],
                        ),
                        trial_status=TrialStatus.done,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[
                                (0, 5),
                                (0, 6),
                                (0, 7),
                                (0, 8),
                                (0, 9),
                            ],
                            ambient_indices=[
                                (0, 5),
                                (0, 6),
                                (0, 7),
                                (0, 8),
                                (0, 9),
                            ],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=10, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=10, step=1),
                            ],
                        ),
                        trial_status=TrialStatus.running,
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                    ),
                ],
                aggregated_parameter_space=None,
            ),
            2,
            id="count only done jagged",
        ),
    ],
)
def test_trial_table_count_grid(
    table: TrialTable,
    expected: int,
) -> None:
    actual = table.count_grid()
    assert actual == expected


@pytest.mark.parametrize(
    "model",
    [
        TrialTableModel(
            trials=[],
            aggregated_parameter_space=None,
        ),
        TrialTableModel(
            trials=[
                TrialModel(
                    study_id="some_study",
                    trial_id="01",
                    reserved_timestamp=DT,
                    trial_status=TrialStatus.running,
                    const_param=None,
                    parameter_space=ParameterAlignedSpaceModel(
                        type="aligned",
                        axes=[
                            LineSegmentModel(
                                type="int",
                                size="0xa",
                                step="0x1",
                                start="0x0",
                                ambient_index="0x0",
                                ambient_size="0x64",
                            ),
                        ],
                        check_lower_filling=True,
                    ),
                    result_type="scalar",
                    result_value_type="float",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            aggregated_parameter_space=None,
        ),
        TrialTableModel(
            trials=[
                TrialModel(
                    study_id="some_study",
                    trial_id="01",
                    reserved_timestamp=DT,
                    trial_status=TrialStatus.running,
                    const_param=None,
                    parameter_space=ParameterAlignedSpaceModel(
                        type="aligned",
                        axes=[
                            LineSegmentModel(
                                type="int",
                                size="0xa",
                                step="0x1",
                                start="0x0",
                                ambient_index="0x0",
                                ambient_size="0x64",
                            ),
                        ],
                        check_lower_filling=True,
                    ),
                    result_type="scalar",
                    result_value_type="float",
                    worker_node_name="w01",
                    worker_node_id="w01",
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(
                                    type="scalar",
                                    value_type="int",
                                    value="0x1",
                                    name="p1",
                                ),
                            ),
                            result=ScalarValue(
                                type="scalar",
                                value_type="float",
                                value="0x1.0000000000000p+1",
                                name="p2",
                            ),
                        ),
                    ],
                ),
            ],
            aggregated_parameter_space=None,
        ),
    ],
)
def test_trial_table_to_model_from_model(model: TrialTableModel) -> None:
    table = TrialTable.from_model(model)
    reconstructed_model = table.to_model()
    assert model == reconstructed_model


@pytest.mark.parametrize(
    ("trial_table", "trial_id", "worker_node_id", "expected"),
    [
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.running,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=100,
                                    start=1,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            "t02",
            "w01",
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=100,
                                    start=1,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=DT,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=100,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=100,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=100,
                                    start=1,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            id="aligned normal",
        ),
        pytest.param(
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 0)],
                            ambient_indices=[(0, 0)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.running,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 1)],
                            ambient_indices=[(0, 1)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 2)],
                            ambient_indices=[(0, 2)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=6,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            "t02",
            "w01",
            TrialTable(
                trials=[
                    Trial(
                        study_id="s01",
                        trial_id="t01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 0)],
                            ambient_indices=[(0, 0)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 1)],
                            ambient_indices=[(0, 1)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=DT,
                    ),
                    Trial(
                        study_id="s01",
                        trial_id="t03",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 2)],
                            ambient_indices=[(0, 2)],
                            axes_info=[
                                DummyLineSegment(type="int", name="x", ambient_size=6, step=1),
                                DummyLineSegment(type="int", name="y", ambient_size=6, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=None,
                        registered_timestamp=None,
                    ),
                ],
                aggregated_parameter_space={
                    -1: [],
                    0: [],
                    1: [
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=2,
                                    ambient_size=6,
                                    start=2,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=0,
                                    ambient_size=6,
                                    start=0,
                                    name="x",
                                ),
                                ParameterRangeInt(
                                    type="int",
                                    size=1,
                                    ambient_index=1,
                                    ambient_size=6,
                                    start=1,
                                    name="y",
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            id="jagged normal",
        ),
    ],
)
def test_trial_table_receipt_trial_result(
    trial_table: TrialTable,
    trial_id: str,
    worker_node_id: str,
    expected: TrialTable,
    mocker: MockFixture,
) -> None:
    _ = mocker.patch("lite_dist2.curriculum_models.trial.publish_timestamp", return_value=DT)

    trial_table.receipt_trial_result(trial_id, worker_node_id)
    actual_model = trial_table.to_model()
    expected_model = expected.to_model()
    assert actual_model.trials == expected_model.trials
    assert actual_model.aggregated_parameter_space == expected_model.aggregated_parameter_space


# noinspection SpellCheckingInspection
def test_trial_table_receipt_trial_result_raise_override_done_trial() -> None:
    trial_table = TrialTable(
        trials=[
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="x"),
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="y"),
                    ],
                    check_lower_filling=True,
                ),
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=[
                    Mapping(
                        params=(
                            ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                            ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                        ),
                        result=ScalarValue(type="scalar", value_type="int", value="0x0", name="p2"),
                    ),
                ],
            ),
        ],
        aggregated_parameter_space={
            -1: [],
            0: [],
            1: [
                ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="x"),
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="y"),
                    ],
                    check_lower_filling=True,
                ),
            ],
        },
    )

    with pytest.raises(LD2ParameterError, match=r"Cannot\soverride\sresult\sof\sdone\strial"):
        trial_table.receipt_trial_result("t01", "w01")


# noinspection SpellCheckingInspection
def test_trial_table_receipt_trial_result_raise_not_found_trial() -> None:
    trial_table = TrialTable(
        trials=[],
        aggregated_parameter_space={
            -1: [],
            0: [],
            1: [],
        },
    )

    with pytest.raises(LD2ParameterError, match=r"Not\sfound\strial\sthat\sid"):
        trial_table.receipt_trial_result("t01", "w01")


# noinspection SpellCheckingInspection
def test_trial_table_receipt_trial_result_raise_unmatch_worker_id() -> None:
    trial_table = TrialTable(
        trials=[
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.running,
                const_param=None,
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="x"),
                        ParameterRangeInt(type="int", size=1, ambient_index=0, ambient_size=100, start=0, name="y"),
                    ],
                    check_lower_filling=True,
                ),
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
            ),
        ],
        aggregated_parameter_space={
            -1: [],
            0: [],
            1: [],
        },
    )

    with pytest.raises(LD2ParameterError, match=r"This\strial\sis\sreserved\sby\sother\sworker"):
        trial_table.receipt_trial_result("t01", "w02")


def test_trial_table_check_timeout_trial() -> None:
    _trial_args = {
        "study_id": "s01",
        "const_param": None,
        "parameter_space": _DUMMY_PARAMETER_SPACE,
        "result_type": "scalar",
        "result_value_type": "int",
        "results": [],
        "worker_node_name": "w01",
        "worker_node_id": "w01",
    }

    now = DT
    trial_table = TrialTable(
        trials=[
            Trial(
                trial_id="running_but_created_now",
                reserved_timestamp=now,
                trial_status=TrialStatus.running,
                **_trial_args,
            ),
            Trial(
                trial_id="running_little_past",
                reserved_timestamp=now - timedelta(seconds=30),
                trial_status=TrialStatus.running,
                **_trial_args,
            ),
            Trial(
                trial_id="running_very_past",
                reserved_timestamp=now - timedelta(seconds=3000),
                trial_status=TrialStatus.running,
                **_trial_args,
            ),
            Trial(
                trial_id="done_little_past",
                reserved_timestamp=now - timedelta(seconds=40),
                trial_status=TrialStatus.done,
                **_trial_args,
            ),
            Trial(
                trial_id="done_very_past",
                reserved_timestamp=now - timedelta(seconds=3000),
                trial_status=TrialStatus.done,
                **_trial_args,
            ),
        ],
        aggregated_parameter_space={},
    )

    expected_trial_table = TrialTable(
        trials=[
            Trial(
                trial_id="running_but_created_now",
                reserved_timestamp=now,
                trial_status=TrialStatus.running,
                **_trial_args,
            ),
            Trial(
                trial_id="running_little_past",
                reserved_timestamp=now - timedelta(seconds=30),
                trial_status=TrialStatus.running,
                **_trial_args,
            ),
            Trial(
                trial_id="done_little_past",
                reserved_timestamp=now - timedelta(seconds=40),
                trial_status=TrialStatus.done,
                **_trial_args,
            ),
            Trial(
                trial_id="done_very_past",
                reserved_timestamp=now - timedelta(seconds=3000),
                trial_status=TrialStatus.done,
                **_trial_args,
            ),
        ],
        aggregated_parameter_space={},
    )
    expected_ids = ["running_very_past"]

    actual_ids = trial_table.check_timeout_trial(now, timeout_seconds=300)
    assert actual_ids == expected_ids
    assert trial_table.to_model() == expected_trial_table.to_model()
