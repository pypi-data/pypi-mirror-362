from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from lite_dist2.curriculum_models.mapping import Mapping, MappingsStorage
from lite_dist2.curriculum_models.trial import TrialModel, TrialStatus
from lite_dist2.expections import LD2NotDoneError
from lite_dist2.study_strategies.base_study_strategy import StudyStrategyParam
from lite_dist2.study_strategies.find_exact_study_strategy import FindExactStudyStrategy
from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.line_segment import LineSegmentModel, ParameterRangeInt
from lite_dist2.value_models.point import ResultType, ScalarValue
from tests.const import DT

if TYPE_CHECKING:
    from lite_dist2.type_definitions import TrialRepositoryType

_DUMMY_PARAMETER_SPACE_MODEL = ParameterAlignedSpaceModel(
    type="aligned",
    axes=[
        LineSegmentModel(
            name="x",
            type="int",
            size="0x2",
            start="0x0",
            ambient_size="0x2",
            ambient_index="0x0",
            step="0x1",
        ),
        LineSegmentModel(
            name="y",
            type="int",
            size="0x2",
            start="0x0",
            ambient_size="0x2",
            ambient_index="0x0",
            step="0x1",
        ),
    ],
    check_lower_filling=True,
)


class MockTrialRepository(BaseTrialRepository):
    def __init__(self) -> None:
        super().__init__(Path("test/s01"))

    @staticmethod
    def get_repository_type() -> TrialRepositoryType:
        return "normal"

    def clean_save_dir(self) -> None:
        pass

    def save(self, trial: TrialModel) -> None:
        pass

    def load(self, trial_id: str) -> TrialModel:
        raise NotImplementedError

    def load_all(self) -> list[TrialModel]:
        raise NotImplementedError

    def delete_save_dir(self) -> None:
        pass


@pytest.fixture
def trial_repository_fixture(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> None:
    return_value = request.param

    # noinspection PyUnusedLocal
    def fake_load_all(self) -> int:  # noqa: ANN001
        return return_value

    monkeypatch.setattr(MockTrialRepository, "load_all", fake_load_all)


@pytest.mark.parametrize(
    ("trial_repository_fixture", "target_value", "expected"),
    [
        pytest.param(
            [],
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            False,
            id="Empty: False",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                        ),
                    ],
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            False,
            id="Not found: False",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
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
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                        ),
                    ],
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            True,
            id="Found: True",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.running,
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
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                        ),
                    ],
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            False,
            id="Found but running: False",
        ),
    ],
    indirect=["trial_repository_fixture"],
)
def test_find_exact_study_strategy_is_done(
    trial_repository_fixture: list[TrialModel],
    target_value: ResultType,
    expected: bool,
) -> None:
    strategy = FindExactStudyStrategy(StudyStrategyParam(target_value=target_value))
    parameter_space = ParameterAlignedSpace(
        axes=[
            ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
            ParameterRangeInt(name="y", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
        ],
        check_lower_filling=True,
    )
    # noinspection PyTypeChecker
    actual = strategy.is_done(None, parameter_space, MockTrialRepository())
    assert actual == expected


@pytest.mark.parametrize(
    ("target_value", "trial_repository_fixture", "expected"),
    [
        pytest.param(
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
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
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                        ),
                    ],
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            MappingsStorage(
                params_info=(
                    ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                    ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                ),
                result_info=ScalarValue(type="scalar", value_type="int", value="0x0"),
                values=[
                    ("0x0", "0x0", "0x64"),
                ],
            ),
            id="Found",
        ),
    ],
    indirect=["trial_repository_fixture"],
)
def test_find_exact_study_strategy_extract_mapping(
    target_value: ResultType,
    trial_repository_fixture: list[TrialModel],
    expected: MappingsStorage,
) -> None:
    repo = MockTrialRepository()
    strategy = FindExactStudyStrategy(StudyStrategyParam(target_value=target_value))
    actual = strategy.extract_mappings(repo)
    assert actual == expected


@pytest.mark.parametrize(
    ("target_value", "trial_repository_fixture"),
    [
        pytest.param(
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            [],
            id="Empty",
        ),
        pytest.param(
            ScalarValue(type="scalar", value_type="int", value="0x64"),
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x65"),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x66"),
                        ),
                    ],
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
            ],
            id="Not found",
        ),
    ],
    indirect=["trial_repository_fixture"],
)
def test_find_exact_study_strategy_extract_mapping_raise(
    target_value: ResultType,
    trial_repository_fixture: list[TrialModel],
) -> None:
    repo = MockTrialRepository()
    strategy = FindExactStudyStrategy(StudyStrategyParam(target_value=target_value))
    with pytest.raises(LD2NotDoneError):
        _ = strategy.extract_mappings(repo)
