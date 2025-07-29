from datetime import datetime

import pytest

from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.curriculum_models.trial import Trial, TrialDoneRecord, TrialModel, TrialStatus
from lite_dist2.expections import LD2NotDoneError
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.jagged_space import ParameterJaggedSpace, ParameterJaggedSpaceModel
from lite_dist2.value_models.line_segment import DummyLineSegment, LineSegmentModel, ParameterRangeInt
from lite_dist2.value_models.point import ResultType, ScalarValue, VectorValue
from tests.const import DT, JST

_dummy_space = ParameterJaggedSpace(
    parameters=[(0, 1)],
    ambient_indices=[(0, 1)],
    axes_info=[DummyLineSegment(name="x", type="int", ambient_size=6, step=1)],
)

_dummy_aligned_space = ParameterAlignedSpace(
    axes=[ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_index=1, ambient_size=10)],
    check_lower_filling=True,
)


def test_trial_done_record_calc_duration_sec() -> None:
    rec = TrialDoneRecord(
        trial_id="t01",
        reserved_timestamp=datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
        worker_node_name="w01",
        worker_node_id="w01",
        registered_timestamp=datetime(2025, 4, 27, 20, 36, 11, 500_000, tzinfo=JST),
        grid_size=120,
    )
    actual = rec.calc_duration_sec()
    expected = 1.5
    assert actual == expected


def test_trial_done_record_calc_grid_per_sec() -> None:
    rec = TrialDoneRecord(
        trial_id="t01",
        reserved_timestamp=datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
        worker_node_name="w01",
        worker_node_id="w01",
        registered_timestamp=datetime(2025, 4, 27, 20, 36, 11, 500_000, tzinfo=JST),
        grid_size=120,
    )
    actual = rec.calc_grid_per_sec()
    expected = 80.0
    assert actual == expected


@pytest.mark.parametrize(
    ("trial", "target", "expected"),
    [
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.running,
                const_param=None,
                parameter_space=_dummy_space,
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=[
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x0"),),
                        result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                    ),
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x1"),),
                        result=ScalarValue(type="scalar", value_type="int", value="0x67"),
                    ),
                ],
            ),
            ScalarValue(type="scalar", value_type="int", value="0x66"),
            None,
            id="not found: running",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_space,
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
            ),
            ScalarValue(type="scalar", value_type="int", value="0x66"),
            None,
            id="not found: none result",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_space,
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=[],
            ),
            ScalarValue(type="scalar", value_type="int", value="0x66"),
            None,
            id="not found: empty result",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_space,
                result_type="scalar",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=[
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x0"),),
                        result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                    ),
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x1"),),
                        result=ScalarValue(type="scalar", value_type="int", value="0x67"),
                    ),
                ],
            ),
            ScalarValue(type="scalar", value_type="int", value="0x66"),
            Mapping(
                params=(ScalarValue(type="scalar", value_type="int", value="0x0"),),
                result=ScalarValue(type="scalar", value_type="int", value="0x66"),
            ),
            id="found: scalar",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t01",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_space,
                result_type="vector",
                result_value_type="int",
                worker_node_name="w01",
                worker_node_id="w01",
                results=[
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x0"),),
                        result=VectorValue(type="vector", value_type="int", values=["0x66", "0x2328"]),
                    ),
                    Mapping(
                        params=(ScalarValue(type="scalar", value_type="int", value="0x1"),),
                        result=VectorValue(type="vector", value_type="int", values=["0x67", "0x2329"]),
                    ),
                ],
            ),
            VectorValue(type="vector", value_type="int", values=["0x66", "0x2328"]),
            Mapping(
                params=(ScalarValue(type="scalar", value_type="int", value="0x0"),),
                result=VectorValue(type="vector", value_type="int", values=["0x66", "0x2328"]),
            ),
            id="found: vector",
        ),
    ],
)
def test_trial_find_target_value(trial: Trial, target: ResultType, expected: Mapping | None) -> None:
    actual = trial.find_target_value(target)
    assert actual == expected


def test_to_done_record() -> None:
    trial = Trial(
        study_id="s01",
        trial_id="t02",
        reserved_timestamp=datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
        trial_status=TrialStatus.done,
        const_param=None,
        parameter_space=_dummy_aligned_space,
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
                        name="x",
                    ),
                ),
                result=ScalarValue(
                    type="scalar",
                    value_type="float",
                    value="0x1.0000000000000p+1",
                    name="r1",
                ),
            ),
            Mapping(
                params=(
                    ScalarValue(
                        type="scalar",
                        value_type="int",
                        value="0x2",
                        name="x",
                    ),
                ),
                result=ScalarValue(
                    type="scalar",
                    value_type="float",
                    value="0x1.0000000000000p+2",
                    name="r1",
                ),
            ),
        ],
        registered_timestamp=datetime(2025, 4, 27, 20, 36, 11, 500, tzinfo=JST),
    )
    expected = TrialDoneRecord(
        trial_id="t02",
        reserved_timestamp=datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
        worker_node_name="w01",
        worker_node_id="w01",
        registered_timestamp=datetime(2025, 4, 27, 20, 36, 11, 500, tzinfo=JST),
        grid_size=2,
    )

    actual = trial.to_done_record()
    assert actual == expected


def test_to_done_record_raises() -> None:
    trial = Trial(
        study_id="s01",
        trial_id="t02",
        reserved_timestamp=datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
        trial_status=TrialStatus.running,
        const_param=None,
        parameter_space=_dummy_aligned_space,
        result_type="scalar",
        result_value_type="float",
        worker_node_name="w01",
        worker_node_id="w01",
        results=None,
        registered_timestamp=None,
    )

    with pytest.raises(LD2NotDoneError):
        _ = trial.to_done_record()


@pytest.mark.parametrize(
    ("trial", "cutoff_datetime", "expected"),
    [
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t02",
                reserved_timestamp=DT,
                trial_status=TrialStatus.running,
                const_param=None,
                parameter_space=_dummy_aligned_space,
                result_type="scalar",
                result_value_type="float",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
                registered_timestamp=None,
            ),
            datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
            False,
            id="Not done (status, registered_datetime): False",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t02",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_aligned_space,
                result_type="scalar",
                result_value_type="float",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
                registered_timestamp=None,
            ),
            datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST),
            False,
            id="Not done (registered_datetime): False",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t02",
                reserved_timestamp=DT,
                trial_status=TrialStatus.running,
                const_param=None,
                parameter_space=_dummy_aligned_space,
                result_type="scalar",
                result_value_type="float",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
                registered_timestamp=DT,
            ),
            datetime(2025, 4, 27, 20, 36, 9, 0, tzinfo=JST),
            False,
            id="Not done (status): False",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t02",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_aligned_space,
                result_type="scalar",
                result_value_type="float",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
                registered_timestamp=datetime(2025, 4, 27, 20, 36, 11, 0, tzinfo=JST),
            ),
            datetime(2025, 4, 27, 20, 36, 12, 0, tzinfo=JST),
            False,
            id="Done, but past: False",
        ),
        pytest.param(
            Trial(
                study_id="s01",
                trial_id="t02",
                reserved_timestamp=DT,
                trial_status=TrialStatus.done,
                const_param=None,
                parameter_space=_dummy_aligned_space,
                result_type="scalar",
                result_value_type="float",
                worker_node_name="w01",
                worker_node_id="w01",
                results=None,
                registered_timestamp=datetime(2025, 4, 27, 20, 36, 12, 0, tzinfo=JST),
            ),
            datetime(2025, 4, 27, 20, 36, 11, 0, tzinfo=JST),
            True,
            id="Done, after cutoff datetime: True",
        ),
    ],
)
def test_done_in_after(trial: Trial, cutoff_datetime: datetime, expected: bool) -> None:
    actual = trial.done_in_after(cutoff_datetime)
    assert actual == expected


@pytest.mark.parametrize(
    "model",
    [
        TrialModel(
            study_id="my_study_id0",
            trial_id="01",
            reserved_timestamp=DT,
            trial_status=TrialStatus.done,
            const_param=None,
            parameter_space=ParameterAlignedSpaceModel(
                type="aligned",
                axes=[
                    LineSegmentModel(
                        name="x",
                        type="bool",
                        size="0x2",
                        step="0x1",
                        start=False,
                        ambient_index="0x0",
                        ambient_size="0x2",
                    ),
                ],
                check_lower_filling=True,
            ),
            result_type="scalar",
            result_value_type="bool",
            worker_node_name="w01",
            worker_node_id="w01",
        ),
        TrialModel(
            study_id="my_study_id1",
            trial_id="01",
            reserved_timestamp=DT,
            trial_status=TrialStatus.done,
            const_param=None,
            parameter_space=ParameterAlignedSpaceModel(
                type="aligned",
                axes=[
                    LineSegmentModel(
                        name="x",
                        type="int",
                        size="0x2",
                        step="0x1",
                        start="0x0",
                        ambient_index="0x0",
                        ambient_size="0x2",
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
                            name="x",
                        ),
                    ),
                    result=ScalarValue(
                        type="scalar",
                        value_type="float",
                        value="0x1.0000000000000p+1",
                        name="r1",
                    ),
                ),
            ],
        ),
        TrialModel(
            study_id="my_study_id2",
            trial_id="02",
            reserved_timestamp=DT,
            trial_status=TrialStatus.done,
            const_param=None,
            parameter_space=ParameterJaggedSpaceModel(
                type="jagged",
                axes_info=[
                    LineSegmentModel(
                        name="x",
                        type="int",
                        size="0x1",
                        start="0x0",
                        step="0x1",
                        ambient_index="0x0",
                        ambient_size="0x1",
                        is_dummy=True,
                    ),
                ],
                parameters=[("0x1",)],
                ambient_indices=[("0x1",)],
            ),
            result_type="scalar",
            result_value_type="int",
            worker_node_name="w01",
            worker_node_id="w01",
        ),
        TrialModel(
            study_id="my_study_id3",
            trial_id="01",
            reserved_timestamp=DT,
            trial_status=TrialStatus.done,
            const_param=None,
            parameter_space=ParameterJaggedSpaceModel(
                type="jagged",
                axes_info=[
                    LineSegmentModel(
                        name="x",
                        type="int",
                        size="0x1",
                        start="0x0",
                        step="0x1",
                        ambient_index="0x0",
                        ambient_size="0x1",
                        is_dummy=True,
                    ),
                ],
                parameters=[("0x1",)],
                ambient_indices=[("0x1",)],
            ),
            result_type="scalar",
            result_value_type="int",
            worker_node_name="w01",
            worker_node_id="w01",
            results=[
                Mapping(
                    params=(
                        ScalarValue(
                            type="scalar",
                            value_type="int",
                            value="0x1",
                            name="x",
                        ),
                    ),
                    result=ScalarValue(
                        type="scalar",
                        value_type="int",
                        value="0x2",
                        name="r1",
                    ),
                ),
            ],
        ),
    ],
)
def test_trial_to_model_from_model(model: TrialModel) -> None:
    trial = Trial.from_model(model)
    reconstructed_trial = trial.to_model()
    assert model == reconstructed_trial
