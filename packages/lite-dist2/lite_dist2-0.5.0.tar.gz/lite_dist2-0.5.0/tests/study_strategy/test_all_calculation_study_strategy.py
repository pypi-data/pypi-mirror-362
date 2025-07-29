from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from lite_dist2.curriculum_models.mapping import Mapping, MappingsStorage
from lite_dist2.curriculum_models.trial import TrialModel, TrialStatus
from lite_dist2.curriculum_models.trial_table import TrialTable
from lite_dist2.expections import LD2NotDoneError
from lite_dist2.study_strategies.all_calculation_study_strategy import AllCalculationStudyStrategy
from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.line_segment import LineSegmentModel, ParameterRangeInt
from lite_dist2.value_models.point import ScalarValue, VectorValue
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
def done_grid_fixture(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> None:
    return_value = request.param

    # noinspection PyUnusedLocal
    def fake_count_grid(self) -> int:  # noqa: ANN001
        return return_value

    monkeypatch.setattr(TrialTable, "count_grid", fake_count_grid)


@pytest.fixture
def all_grid_fixture(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> None:
    return_value = request.param

    # noinspection PyUnusedLocal
    def fake_get_total(self) -> int:  # noqa: ANN001
        return return_value

    monkeypatch.setattr(ParameterAlignedSpace, "get_total", fake_get_total)


@pytest.mark.parametrize(
    ("done_grid_fixture", "all_grid_fixture", "expected"),
    [
        pytest.param(10, 10, True, id="Done"),
        pytest.param(9, 10, False, id="Yet"),
    ],
    indirect=["done_grid_fixture", "all_grid_fixture"],
)
def test_all_calculation_study_strategy_is_done(
    done_grid_fixture: int,
    all_grid_fixture: int,
    expected: bool,
) -> None:
    strategy = AllCalculationStudyStrategy(study_strategy_param=None)
    trial_table = TrialTable(trials=[], aggregated_parameter_space=None)
    parameter_space = ParameterAlignedSpace(
        axes=[
            ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
            ParameterRangeInt(name="y", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
        ],
        check_lower_filling=True,
    )
    actual = strategy.is_done(trial_table, parameter_space, MockTrialRepository())
    assert actual == expected


@pytest.fixture
def trial_repository_fixture(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> None:
    return_value = request.param

    # noinspection PyUnusedLocal
    def fake_load_all(self) -> int:  # noqa: ANN001
        return return_value

    monkeypatch.setattr(MockTrialRepository, "load_all", fake_load_all)


@pytest.mark.parametrize(
    ("trial_repository_fixture", "expected"),
    [
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x67"),
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
                    ("0x1", "0x1", "0x67"),
                ],
            ),
            id="Single trial, single map",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x67"),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x68"),
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
                TrialModel(
                    trial_id="t02",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x3", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x69"),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x4", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x6a"),
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
                    ("0x1", "0x1", "0x67"),
                    ("0x2", "0x2", "0x68"),
                    ("0x3", "0x3", "0x69"),
                    ("0x4", "0x4", "0x6a"),
                ],
            ),
            id="Multi trial, multi map, scalar",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                            ),
                            result=VectorValue(type="vector", value_type="int", values=["0x67", "0x67"]),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                            ),
                            result=VectorValue(type="vector", value_type="int", values=["0x68", "0x68"]),
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
                TrialModel(
                    trial_id="t02",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x3", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x3", name="y"),
                            ),
                            result=VectorValue(type="vector", value_type="int", values=["0x69", "0x69"]),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x4", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x4", name="y"),
                            ),
                            result=VectorValue(type="vector", value_type="int", values=["0x6a", "0x6a"]),
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
                result_info=VectorValue(type="vector", value_type="int", values=["0x0", "0x0"]),
                values=[
                    ("0x1", "0x1", "0x67", "0x67"),
                    ("0x2", "0x2", "0x68", "0x68"),
                    ("0x3", "0x3", "0x69", "0x69"),
                    ("0x4", "0x4", "0x6a", "0x6a"),
                ],
            ),
            id="Multi trial, multi map, vector",
        ),
    ],
    indirect=["trial_repository_fixture"],
)
def test_find_exact_study_strategy_extract_mapping(
    trial_repository_fixture: list[TrialModel],
    expected: MappingsStorage,
) -> None:
    repo = MockTrialRepository()
    strategy = AllCalculationStudyStrategy(None)
    actual = strategy.extract_mappings(repo)
    assert actual == expected


@pytest.mark.parametrize(
    "trial_repository_fixture",
    [
        pytest.param(
            [],
            id="Empty",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=None,
                    study_id="s01",
                    reserved_timestamp=DT,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE_MODEL,
                    result_type="scalar",
                    result_value_type="int",
                    worker_node_name="w01",
                    worker_node_id="w01",
                ),
                TrialModel(
                    trial_id="t02",
                    trial_status=TrialStatus.done,
                    results=None,
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
            id="None first",
        ),
        pytest.param(
            [
                TrialModel(
                    trial_id="t01",
                    trial_status=TrialStatus.done,
                    results=[
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x67"),
                        ),
                        Mapping(
                            params=(
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="x"),
                                ScalarValue(type="scalar", value_type="int", value="0x2", name="y"),
                            ),
                            result=ScalarValue(type="scalar", value_type="int", value="0x68"),
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
                TrialModel(
                    trial_id="t02",
                    trial_status=TrialStatus.done,
                    results=None,
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
            id="None",
        ),
    ],
    indirect=["trial_repository_fixture"],
)
def test_find_exact_study_strategy_extract_mapping_raise(
    trial_repository_fixture: list[TrialModel],
) -> None:
    repo = MockTrialRepository()
    strategy = AllCalculationStudyStrategy(None)
    with pytest.raises(LD2NotDoneError):
        _ = strategy.extract_mappings(repo)
