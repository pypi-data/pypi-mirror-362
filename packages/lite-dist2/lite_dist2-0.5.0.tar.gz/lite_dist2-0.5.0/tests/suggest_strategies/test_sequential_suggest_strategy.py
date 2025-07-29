import pytest

from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.curriculum_models.trial import Trial, TrialStatus
from lite_dist2.curriculum_models.trial_table import TrialTable
from lite_dist2.expections import LD2ParameterError
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyParam
from lite_dist2.suggest_strategies.sequential_suggest_strategy import SequentialSuggestStrategy
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace
from lite_dist2.value_models.base_space import ParameterSpace
from lite_dist2.value_models.jagged_space import ParameterJaggedSpace
from lite_dist2.value_models.line_segment import DummyLineSegment, ParameterRangeInt
from lite_dist2.value_models.point import ScalarValue
from tests.const import DT


@pytest.mark.parametrize(
    ("strategy", "start", "max_num", "expected"),
    [
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            0,
            3,
            ParameterJaggedSpace(
                parameters=[(0,), (1,), (2,)],
                ambient_indices=[(0,), (1,), (2,)],
                axes_info=[DummyLineSegment(name="x", type="int", ambient_size=6, step=1)],
            ),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            3,
            3,
            ParameterJaggedSpace(
                parameters=[(3,), (4,), (5,)],
                ambient_indices=[(3,), (4,), (5,)],
                axes_info=[DummyLineSegment(name="x", type="int", ambient_size=6, step=1)],
            ),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            4,
            3,
            ParameterJaggedSpace(
                parameters=[(4,), (5,)],
                ambient_indices=[(4,), (5,)],
                axes_info=[DummyLineSegment(name="x", type="int", ambient_size=6, step=1)],
            ),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=3, start=0, ambient_size=6, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            0,
            3,
            ParameterJaggedSpace(
                parameters=[(0, 0), (0, 1), (0, 2)],
                ambient_indices=[(0, 0), (0, 1), (0, 2)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                    DummyLineSegment(name="y", type="int", ambient_size=6, step=1),
                ],
            ),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=3, start=0, ambient_size=6, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            5,
            3,
            ParameterJaggedSpace(
                parameters=[(0, 5), (1, 0), (1, 1)],
                ambient_indices=[(0, 5), (1, 0), (1, 1)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                    DummyLineSegment(name="y", type="int", ambient_size=6, step=1),
                ],
            ),
        ),
    ],
)
def test_sequential_suggest_strategy_jagged_suggest(
    strategy: SequentialSuggestStrategy,
    start: int,
    max_num: int,
    expected: ParameterJaggedSpace,
) -> None:
    actual = strategy._jagged_suggest(start, max_num)
    assert actual == expected


@pytest.mark.parametrize(
    ("strategy", "flatten_index", "expected"),
    [
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),  # 使わない
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            0,
            (1, 2, 3, 4, 5, 6),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            2,
            (3, 4, 5, 6),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=7, start=0, ambient_size=7, ambient_index=0),
                        ParameterRangeInt(type="int", size=3, start=0, ambient_size=3, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            0,
            (1, 2, 3, 6, 9, 12, 15, 18, 21),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=7, start=0, ambient_size=7, ambient_index=0),
                        ParameterRangeInt(type="int", size=3, start=0, ambient_size=3, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            1,
            (2, 3),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=7, start=0, ambient_size=7, ambient_index=0),
                        ParameterRangeInt(type="int", size=3, start=0, ambient_size=3, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            4,
            (5, 6),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            876,
            (877, 878, 879, 880),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            800,
            (801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 1000),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            790,
            (791, 792, 793, 794, 795, 796, 797, 798, 799, 800),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            799,
            (800,),
        ),
    ],
)
def test_sequential_suggest_strategy_generate_available_next_finite(
    strategy: SequentialSuggestStrategy,
    flatten_index: int,
    expected: tuple[int, ...],
) -> None:
    actual = strategy._generate_available_next_finite(flatten_index)
    assert actual == expected


@pytest.mark.parametrize(
    ("strategy", "flatten_index", "expected"),
    [
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            0,
            ((1,), True),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            4,
            ((5,), True),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            4,
            ((5, 6, 7, 8, 9, 10), False),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            9,
            ((10,), False),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            10,
            ((11, 12, 13, 14, 15, 16, 17, 18, 19, 20), True),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            10,
            ((11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90, 100), False),
        ),
        (
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(type="int", size=None, start=0, ambient_size=None, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                        ParameterRangeInt(type="int", size=10, start=0, ambient_size=10, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            100,
            ((101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200), True),
        ),
    ],
)
def test_sequential_suggest_strategy_generate_available_next_infinite(
    strategy: SequentialSuggestStrategy,
    flatten_index: int,
    expected: tuple[tuple[int, ...], bool],
) -> None:
    actual = strategy._generate_available_next_infinite(flatten_index)
    assert actual == expected


@pytest.mark.parametrize(
    ("init", "ratio", "iter_num", "expected"),
    [
        ((1, 2, 3), 3, 5, (1, 2, 3, 6, 9)),
        ((1, 2, 3, 4), 10, 3, (1, 2, 3)),
    ],
)
def test_sequential_suggest_strategy_infinite_available_generator(
    init: tuple[int, ...],
    ratio: int,
    iter_num: int,
    expected: tuple[int, ...],
) -> None:
    generator = SequentialSuggestStrategy._infinite_available_generator(init, ratio)
    actual = []
    for i, v in enumerate(generator):
        if i >= iter_num:
            break
        actual.append(v)
    actual = tuple(actual)
    assert actual == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 1),
        (None, 2, 2),
        (3, None, 3),
    ],
)
def test_sequential_suggest_strategy_nullable_min(a: int | None, b: int | None, expected: int) -> None:
    actual = SequentialSuggestStrategy._nullable_min(a, b)
    assert actual == expected


def test_sequential_suggest_strategy_nullable_min_raise_both_none() -> None:
    with pytest.raises(LD2ParameterError, match=r"both\sis\sNone"):
        _ = SequentialSuggestStrategy._nullable_min(None, None)


@pytest.mark.parametrize(
    ("strategy", "trial_table", "max_num", "expected"),
    [
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[],
                aggregated_parameter_space={-1: [], 0: []},
            ),
            3,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=3, start=0, ambient_size=6, ambient_index=0),
                ],
                check_lower_filling=True,
            ),
            id="1D init",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x2", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                            ),
                        ],
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
                                    size=3,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            3,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=3, start=3, ambient_size=6, ambient_index=3),
                ],
                check_lower_filling=True,
            ),
            id="1D continuing",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(
                            name="x",
                            type="int",
                            size=None,
                            start=0,
                            ambient_size=None,
                            ambient_index=0,
                        ),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[],
                aggregated_parameter_space={-1: [], 0: []},
            ),
            3,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=3, start=0, ambient_size=None, ambient_index=0),
                ],
                check_lower_filling=True,
            ),
            id="1D init infinite",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(
                            name="x",
                            type="int",
                            size=None,
                            start=0,
                            ambient_size=None,
                            ambient_index=0,
                        ),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=None,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(ScalarValue(type="scalar", value_type="int", value="0x2", name="x"),),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                            ),
                        ],
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
                                    size=3,
                                    start=0,
                                    ambient_size=None,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            3,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=3, start=3, ambient_size=None, ambient_index=3),
                ],
                check_lower_filling=True,
            ),
            id="1D continuing infinite",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=4, start=0, ambient_size=4, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 0), (0, 1), (0, 2)],
                            ambient_indices=[(0, 0), (0, 1), (0, 2)],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                            ],
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
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
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
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=4,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            4,
            ParameterJaggedSpace(
                parameters=[(0, 3), (1, 0), (1, 1), (1, 2)],
                ambient_indices=[(0, 3), (1, 0), (1, 1), (1, 2)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                    DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                ],
            ),
            id="2D continuing",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=4, start=0, ambient_size=4, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 0), (0, 1), (0, 2)],
                            ambient_indices=[(0, 0), (0, 1), (0, 2)],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                            ],
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
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(1, 1), (1, 2), (1, 3)],
                            ambient_indices=[(1, 1), (1, 2), (1, 3)],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                            ],
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x69"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x6a"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x6b"),
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
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=4,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=1,
                                    ambient_size=6,
                                    ambient_index=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=1,
                                    ambient_size=4,
                                    ambient_index=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            4,
            ParameterJaggedSpace(
                parameters=[(0, 3), (1, 0)],
                ambient_indices=[(0, 3), (1, 0)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                    DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                ],
            ),
            id="2D striping",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=6, start=0, ambient_size=6, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=4, start=0, ambient_size=4, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=4,
                                    ambient_index=0,
                                ),
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
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                            ),
                        ],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=1,
                                    ambient_size=6,
                                    ambient_index=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=1,
                                    ambient_size=4,
                                    ambient_index=1,
                                ),
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
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x69"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x6a"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x6b"),
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
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=6,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=4,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=1,
                                    ambient_size=6,
                                    ambient_index=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=1,
                                    ambient_size=4,
                                    ambient_index=1,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            4,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=1, start=0, ambient_size=6, ambient_index=0),
                    ParameterRangeInt(name="y", type="int", size=1, start=3, ambient_size=4, ambient_index=3),
                ],
                check_lower_filling=True,
            ),
            id="2D striping force aligned",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=False),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(
                            name="x",
                            type="int",
                            size=None,
                            start=0,
                            ambient_size=None,
                            ambient_index=0,
                        ),
                        ParameterRangeInt(
                            name="y",
                            type="int",
                            size=4,
                            start=0,
                            ambient_size=4,
                            ambient_index=0,
                        ),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterJaggedSpace(
                            parameters=[(0, 0), (0, 1), (0, 2)],
                            ambient_indices=[(0, 0), (0, 1), (0, 2)],
                            axes_info=[
                                DummyLineSegment(name="x", type="int", ambient_size=6, step=1),
                                DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                            ],
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
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
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
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=None,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=3,
                                    start=0,
                                    ambient_size=4,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                },
            ),
            4,
            ParameterJaggedSpace(
                parameters=[(0, 3), (1, 0), (1, 1), (1, 2)],
                ambient_indices=[(0, 3), (1, 0), (1, 1), (1, 2)],
                axes_info=[
                    DummyLineSegment(name="x", type="int", ambient_size=None, step=1),
                    DummyLineSegment(name="y", type="int", ambient_size=4, step=1),
                ],
            ),
            id="2D continuing infinite",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=2,
                                    start=0,
                                    ambient_size=2,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=2,
                                    start=0,
                                    ambient_size=2,
                                    ambient_index=0,
                                ),
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
                                result=ScalarValue(type="scalar", value_type="int", value="0x64"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                            ),
                            Mapping(
                                params=(
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                    ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                ),
                                result=ScalarValue(type="scalar", value_type="int", value="0x67"),
                            ),
                        ],
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
                                    start=0,
                                    ambient_size=2,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=2,
                                    start=0,
                                    ambient_size=2,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=1,
                                    ambient_size=2,
                                    ambient_index=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=2,
                                    start=0,
                                    ambient_size=2,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    1: [],
                },
            ),
            4,
            None,
            id="2D full",
        ),
        pytest.param(
            SequentialSuggestStrategy(
                suggest_parameter=SuggestStrategyParam(strict_aligned=True),
                parameter_space=ParameterAlignedSpace(
                    axes=[
                        ParameterRangeInt(name="x", type="int", size=51, start=0, ambient_size=51, ambient_index=0),
                        ParameterRangeInt(name="y", type="int", size=51, start=0, ambient_size=51, ambient_index=0),
                    ],
                    check_lower_filling=True,
                ),
            ),
            TrialTable(
                trials=[
                    Trial(
                        study_id="01",
                        trial_id="00",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="01",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=1,
                                    ambient_size=51,
                                    ambient_index=1,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w02",
                        worker_node_id="w02",
                        results=[],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="02",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=2,
                                    ambient_size=51,
                                    ambient_index=2,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="03",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=3,
                                    ambient_size=51,
                                    ambient_index=3,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="04",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.running,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=4,
                                    ambient_size=51,
                                    ambient_index=4,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w02",
                        worker_node_id="w02",
                        results=None,
                    ),
                    Trial(
                        study_id="01",
                        trial_id="05",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=5,
                                    ambient_size=51,
                                    ambient_index=5,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[],
                    ),
                    Trial(
                        study_id="01",
                        trial_id="06",
                        reserved_timestamp=DT,
                        trial_status=TrialStatus.done,
                        const_param=None,
                        parameter_space=ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=6,
                                    ambient_size=51,
                                    ambient_index=6,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        result_type="scalar",
                        result_value_type="int",
                        worker_node_name="w01",
                        worker_node_id="w01",
                        results=[],
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
                                    start=6,
                                    ambient_size=51,
                                    ambient_index=6,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=4,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                        ParameterAlignedSpace(
                            axes=[
                                ParameterRangeInt(
                                    name="x",
                                    type="int",
                                    size=1,
                                    start=5,
                                    ambient_size=51,
                                    ambient_index=5,
                                ),
                                ParameterRangeInt(
                                    name="y",
                                    type="int",
                                    size=51,
                                    start=0,
                                    ambient_size=51,
                                    ambient_index=0,
                                ),
                            ],
                            check_lower_filling=True,
                        ),
                    ],
                    1: [],
                },
            ),
            51,
            ParameterAlignedSpace(
                axes=[
                    ParameterRangeInt(name="x", type="int", size=1, start=7, ambient_size=51, ambient_index=7),
                    ParameterRangeInt(name="y", type="int", size=51, start=0, ambient_size=51, ambient_index=0),
                ],
                check_lower_filling=True,
            ),
            id="2D 2 node",
        ),
    ],
)
def test_sequential_suggest_strategy_suggest(
    strategy: SequentialSuggestStrategy,
    trial_table: TrialTable,
    max_num: int,
    expected: ParameterSpace | None,
) -> None:
    actual = strategy.suggest(trial_table, max_num)
    assert actual == expected
