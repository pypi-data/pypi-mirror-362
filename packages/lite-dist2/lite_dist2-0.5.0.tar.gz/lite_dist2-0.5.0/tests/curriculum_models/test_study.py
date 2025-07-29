import threading
from pathlib import Path

import pytest

from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.curriculum_models.study import Study
from lite_dist2.curriculum_models.study_portables import StudyModel
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.curriculum_models.trial import TrialModel, TrialStatus
from lite_dist2.curriculum_models.trial_table import TrialTable, TrialTableModel
from lite_dist2.study_strategies import StudyStrategyModel
from lite_dist2.study_strategies.all_calculation_study_strategy import AllCalculationStudyStrategy
from lite_dist2.suggest_strategies import SequentialSuggestStrategy
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyModel, SuggestStrategyParam
from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
from lite_dist2.trial_repositories.trial_repository_model import TrialRepositoryModel
from lite_dist2.type_definitions import TrialRepositoryType
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.line_segment import (
    LineSegmentModel,
    ParameterRangeFloat,
)
from lite_dist2.value_models.point import ScalarValue
from tests.const import DT


@pytest.mark.parametrize(
    "model",
    [
        pytest.param(
            StudyModel(
                study_id="01",
                name="s1",
                required_capacity=set(),
                status=StudyStatus.running,
                registered_timestamp=DT,
                study_strategy=StudyStrategyModel(type="all_calculation", study_strategy_param=None),
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
                            step="0x1",
                            start="0x0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                        LineSegmentModel(
                            name="y",
                            type="int",
                            size="0x64",
                            step="0x1",
                            start="0x0",
                            ambient_size="0x64",
                            ambient_index="0x0",
                        ),
                    ],
                    check_lower_filling=True,
                ),
                result_type="scalar",
                result_value_type="int",
                trial_table=TrialTableModel(
                    trials=[
                        TrialModel(
                            study_id="01",
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
                                        size="0x1",
                                        step="0x1",
                                        start="0x0",
                                        ambient_size="0x64",
                                        ambient_index="0x0",
                                    ),
                                    LineSegmentModel(
                                        name="y",
                                        type="int",
                                        size="0x2",
                                        step="0x1",
                                        start="0x0",
                                        ambient_size="0x64",
                                        ambient_index="0x0",
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
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                    ),
                                    result=ScalarValue(
                                        type="scalar",
                                        value_type="float",
                                        value="0x1.0000000000000p-1",
                                    ),
                                ),
                                Mapping(
                                    params=(
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                        ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                    ),
                                    result=ScalarValue(
                                        type="scalar",
                                        value_type="float",
                                        value="0x1.0000000000000p-2",
                                    ),
                                ),
                            ],
                        ),
                        TrialModel(
                            study_id="01",
                            trial_id="01",
                            reserved_timestamp=DT,
                            trial_status=TrialStatus.running,
                            const_param=None,
                            parameter_space=ParameterAlignedSpaceModel(
                                type="aligned",
                                axes=[
                                    LineSegmentModel(
                                        name="x",
                                        type="int",
                                        size="0x1",
                                        step="0x1",
                                        start="0x0",
                                        ambient_size="0x64",
                                        ambient_index="0x0",
                                    ),
                                    LineSegmentModel(
                                        name="y",
                                        type="int",
                                        size="0x2",
                                        step="0x1",
                                        start="0x2",
                                        ambient_size="0x64",
                                        ambient_index="0x2",
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
                    aggregated_parameter_space={
                        -1: [],
                        0: [
                            ParameterAlignedSpaceModel(
                                type="aligned",
                                axes=[
                                    LineSegmentModel(
                                        name="x",
                                        type="int",
                                        size="0x1",
                                        step="0x1",
                                        start="0x0",
                                        ambient_size="0x64",
                                        ambient_index="0x0",
                                    ),
                                    LineSegmentModel(
                                        name="y",
                                        type="int",
                                        size="0x2",
                                        step="0x1",
                                        start="0x0",
                                        ambient_size="0x64",
                                        ambient_index="0x0",
                                    ),
                                ],
                                check_lower_filling=True,
                            ),
                        ],
                    },
                ),
                trial_repository=TrialRepositoryModel(
                    type="normal",
                    save_dir=Path("test/01"),
                ),
            ),
            id="full_definition",
        ),
    ],
)
def test_study_to_model_from_model(model: StudyModel) -> None:
    study = Study.from_model(model)
    reconstructed = study.to_model()
    assert model == reconstructed


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
        return []

    def delete_save_dir(self) -> None:
        pass


def test_study_suggest_receipt_single_thread() -> None:
    _parameter_space = ParameterAlignedSpace(
        axes=[
            ParameterRangeFloat(
                name="x",
                type="float",
                size=20,
                step=0.5,
                start=0.0,
                ambient_index=0,
                ambient_size=20,
            ),
            ParameterRangeFloat(
                name="y",
                type="float",
                size=20,
                step=0.5,
                start=0.0,
                ambient_index=0,
                ambient_size=20,
            ),
        ],
        check_lower_filling=True,
    )
    study = Study(
        study_id="s01",
        name="synchronous_test",
        required_capacity=set(),
        status=StudyStatus.running,
        registered_timestamp=DT,
        study_strategy=AllCalculationStudyStrategy(study_strategy_param=None),
        suggest_strategy=SequentialSuggestStrategy(
            suggest_parameter=SuggestStrategyParam(strict_aligned=True),
            parameter_space=_parameter_space,
        ),
        const_param=None,
        parameter_space=_parameter_space,
        result_type="scalar",
        result_value_type="float",
        trial_table=TrialTable(trials=[], aggregated_parameter_space=None),
        trial_repository=MockTrialRepository(),
    )

    def contract_and_submit() -> None:
        # trial 取得
        trial = study.suggest_next_trial(num=5, worker_node_name="w01", worker_node_id="w01")
        if trial is None:
            return

        # 結果書き込み
        raw_mappings = []
        for parameter in trial.parameter_space.grid():
            dummy_result = 0.5
            raw_mappings.append((parameter, dummy_result))
        trial.set_result(trial.convert_mappings_from(raw_mappings))

        # trial 送信
        study.receipt_trial(trial)

    while not study.is_done():
        contract_and_submit()

    expected_trial_num = 80  # 20*20/5
    assert study.trial_table.count_trial() == expected_trial_num


def test_study_suggest_receipt_multi_threads_synchronous() -> None:
    _parameter_space = ParameterAlignedSpace(
        axes=[
            ParameterRangeFloat(
                name="x",
                type="float",
                size=20,
                step=0.5,
                start=0.0,
                ambient_index=0,
                ambient_size=20,
            ),
            ParameterRangeFloat(
                name="y",
                type="float",
                size=20,
                step=0.5,
                start=0.0,
                ambient_index=0,
                ambient_size=20,
            ),
        ],
        check_lower_filling=True,
    )
    study = Study(
        study_id="s01",
        name="synchronous_test",
        required_capacity=set(),
        status=StudyStatus.running,
        registered_timestamp=DT,
        study_strategy=AllCalculationStudyStrategy(study_strategy_param=None),
        suggest_strategy=SequentialSuggestStrategy(
            suggest_parameter=SuggestStrategyParam(strict_aligned=True),
            parameter_space=_parameter_space,
        ),
        const_param=None,
        parameter_space=_parameter_space,
        result_type="scalar",
        result_value_type="float",
        trial_table=TrialTable(trials=[], aggregated_parameter_space=None),
        trial_repository=MockTrialRepository(),
    )

    def contract_and_submit() -> None:
        # trial 取得
        trial = study.suggest_next_trial(num=5, worker_node_name="w01", worker_node_id="w01")

        # 結果書き込み
        raw_mappings = []
        for parameter in trial.parameter_space.grid():
            dummy_result = 0.5
            raw_mappings.append((parameter, dummy_result))
        trial.set_result(trial.convert_mappings_from(raw_mappings))

        # trial 送信
        study.receipt_trial(trial)

    # スレッドを複数作成

    num_threads = 10
    while not study.is_done():
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=contract_and_submit, name=f"Thread-{i + 1}")
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    expected_trial_num = 80  # 20*20/5
    assert study.trial_table.count_trial() == expected_trial_num
