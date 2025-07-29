from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from lite_dist2.curriculum_models.mapping import MappingsStorage
from lite_dist2.curriculum_models.study_portables import StudyModel, StudyRegistry, StudyStorage, StudySummary
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.study_strategies import StudyStrategyModel
from lite_dist2.study_strategies.base_study_strategy import StudyStrategyParam
from lite_dist2.suggest_strategies import SuggestStrategyModel
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyParam
from lite_dist2.trial_repositories.trial_repository_model import TrialRepositoryModel
from lite_dist2.value_models.aligned_space import ParameterAlignedSpaceModel
from lite_dist2.value_models.aligned_space_registry import LineSegmentRegistry, ParameterAlignedSpaceRegistry
from lite_dist2.value_models.line_segment import LineSegmentModel
from lite_dist2.value_models.point import ScalarValue, VectorValue
from tests.const import DT

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


@pytest.mark.parametrize(
    ("registry", "expected"),
    [
        (
            StudyRegistry(
                name="test_registry",
                required_capacity={"test"},
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=VectorValue(
                            type="vector",
                            value_type="int",
                            name="test_target",
                            values=["0x0", "0x1", "0x2"],
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceRegistry(
                    type="aligned",
                    axes=[
                        LineSegmentRegistry(name="x", type="int", size="0x64", step="0x2", start="0x0"),
                        LineSegmentRegistry(name="y", type="float", size="0x64", step="0x1.0p-1", start="0x0.0p+0"),
                    ],
                ),
                result_type="vector",
                result_value_type="int",
            ),
            StudyModel(
                study_id="test_study_id",
                name="test_registry",
                required_capacity={"test"},
                status=StudyStatus.wait,
                registered_timestamp=DT,
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=VectorValue(
                            type="vector",
                            value_type="int",
                            name="test_target",
                            values=["0x0", "0x1", "0x2"],
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceModel(
                    type="aligned",
                    axes=[
                        LineSegmentModel(
                            name="x",
                            type="int",
                            size="0x64",
                            step="0x2",
                            start="0x0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                        LineSegmentModel(
                            name="y",
                            type="float",
                            size="0x64",
                            step="0x1.0p-1",
                            start="0x0.0p+0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                    ],
                    check_lower_filling=True,
                ),
                result_type="vector",
                result_value_type="int",
                trial_repository=TrialRepositoryModel(
                    type="normal",
                    save_dir=Path("test/test_study_id"),
                ),
            ),
        ),
    ],
)
def test_study_registry_to_study_model(registry: StudyRegistry, expected: StudyModel, mocker: MockerFixture) -> None:
    mocker.patch(
        "lite_dist2.curriculum_models.study_portables.StudyRegistry._publish_study_id",
        return_value="test_study_id",
    )
    mocker.patch("lite_dist2.curriculum_models.study_portables.publish_timestamp", return_value=DT)
    actual = registry.to_study_model(trial_file_dir=Path("test"))
    assert actual == expected


@pytest.mark.parametrize(
    ("study_registry", "expected"),
    [
        pytest.param(
            StudyRegistry(
                name="test_registry",
                required_capacity={"test"},
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=VectorValue(
                            type="vector",
                            value_type="int",
                            name="test_target",
                            values=["0x0", "0x1", "0x2"],
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceRegistry(
                    type="aligned",
                    axes=[
                        LineSegmentRegistry(name="x", type="int", size="0x64", step="0x2", start="0x0"),
                        LineSegmentRegistry(name="y", type="float", size="0x64", step="0x1.0p-1", start="0x0.0p+0"),
                    ],
                ),
                result_type="vector",
                result_value_type="int",
            ),
            True,
            id="find_exact, finite: True",
        ),
        pytest.param(
            StudyRegistry(
                name="test_registry",
                required_capacity={"test"},
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=VectorValue(
                            type="vector",
                            value_type="int",
                            name="test_target",
                            values=["0x0", "0x1", "0x2"],
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceRegistry(
                    type="aligned",
                    axes=[
                        LineSegmentRegistry(name="x", type="int", size=None, step="0x2", start="0x0"),
                        LineSegmentRegistry(name="y", type="float", size="0x64", step="0x1.0p-1", start="0x0.0p+0"),
                    ],
                ),
                result_type="vector",
                result_value_type="int",
            ),
            True,
            id="find_exact, infinite: True",
        ),
        pytest.param(
            StudyRegistry(
                name="test_registry",
                required_capacity={"test"},
                study_strategy=StudyStrategyModel(
                    type="all_calculation",
                    study_strategy_param=None,
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceRegistry(
                    type="aligned",
                    axes=[
                        LineSegmentRegistry(name="x", type="int", size="0x64", step="0x2", start="0x0"),
                        LineSegmentRegistry(name="y", type="float", size="0x64", step="0x1.0p-1", start="0x0.0p+0"),
                    ],
                ),
                result_type="vector",
                result_value_type="int",
            ),
            True,
            id="all_calculation, finite: True",
        ),
        pytest.param(
            StudyRegistry(
                name="test_registry",
                required_capacity={"test"},
                study_strategy=StudyStrategyModel(
                    type="all_calculation",
                    study_strategy_param=None,
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=ParameterAlignedSpaceRegistry(
                    type="aligned",
                    axes=[
                        LineSegmentRegistry(name="x", type="int", size=None, step="0x2", start="0x0"),
                        LineSegmentRegistry(name="y", type="float", size="0x64", step="0x1.0p-1", start="0x0.0p+0"),
                    ],
                ),
                result_type="vector",
                result_value_type="int",
            ),
            False,
            id="all_calculation, infinite: False",
        ),
    ],
)
def test_study_registry_is_valid(study_registry: StudyRegistry, expected: bool) -> None:
    actual = study_registry.is_valid()
    assert actual == expected


@pytest.mark.parametrize(
    ("storage", "expected"),
    [
        pytest.param(
            StudyStorage(
                study_id="test_1",
                name="test_name",
                required_capacity={"matrix"},
                registered_timestamp=DT,
                const_param=None,
                parameter_space=ParameterAlignedSpaceModel(
                    type="aligned",
                    axes=[
                        LineSegmentModel(
                            name="x",
                            type="int",
                            size="0x64",
                            step="0x2",
                            start="0x0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                        LineSegmentModel(
                            name="y",
                            type="float",
                            size="0x64",
                            step="0x1.0p-1",
                            start="0x0.0p+0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                    ],
                    check_lower_filling=True,
                ),
                done_timestamp=DT + timedelta(days=1),
                results=MappingsStorage(
                    params_info=(
                        ScalarValue(type="scalar", name="x", value_type="int", value="0x0"),
                        ScalarValue(type="scalar", name="y", value_type="float", value="0x0.0p+0"),
                    ),
                    result_info=ScalarValue(type="scalar", value_type="bool", value=False),
                    values=[
                        ("0x0", "0x0.0p+0", True),
                    ],
                ),
                result_type="scalar",
                result_value_type="bool",
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=ScalarValue(
                            type="scalar",
                            value_type="bool",
                            value=True,
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                done_grids=10000,
                trial_repository=TrialRepositoryModel(
                    type="normal",
                    save_dir=Path("test/test_1"),
                ),
            ),
            StudySummary(
                study_id="test_1",
                name="test_name",
                status=StudyStatus.done,
                required_capacity={"matrix"},
                registered_timestamp=DT,
                const_param=None,
                parameter_space=ParameterAlignedSpaceModel(
                    type="aligned",
                    axes=[
                        LineSegmentModel(
                            name="x",
                            type="int",
                            size="0x64",
                            step="0x2",
                            start="0x0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                        LineSegmentModel(
                            name="y",
                            type="float",
                            size="0x64",
                            step="0x1.0p-1",
                            start="0x0.0p+0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                    ],
                    check_lower_filling=True,
                ),
                result_type="scalar",
                result_value_type="bool",
                study_strategy=StudyStrategyModel(
                    type="find_exact",
                    study_strategy_param=StudyStrategyParam(
                        target_value=ScalarValue(
                            type="scalar",
                            value_type="bool",
                            value=True,
                        ),
                    ),
                ),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                total_grids=10000,
                done_grids=10000,
            ),
        ),
    ],
)
def test_study_storage_to_summary(storage: StudyStorage, expected: StudySummary) -> None:
    actual = storage.to_summary()
    assert actual == expected
