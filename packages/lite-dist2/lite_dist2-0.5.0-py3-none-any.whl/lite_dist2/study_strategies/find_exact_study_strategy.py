from __future__ import annotations

from typing import TYPE_CHECKING

from lite_dist2.curriculum_models.mapping import MappingsStorage
from lite_dist2.curriculum_models.trial import Trial
from lite_dist2.expections import LD2NotDoneError
from lite_dist2.study_strategies import BaseStudyStrategy, StudyStrategyModel

if TYPE_CHECKING:
    from lite_dist2.curriculum_models.mapping import Mapping
    from lite_dist2.curriculum_models.trial_table import TrialTable
    from lite_dist2.study_strategies.base_study_strategy import StudyStrategyParam
    from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
    from lite_dist2.value_models.aligned_space import ParameterAlignedSpace


class FindExactStudyStrategy(BaseStudyStrategy):
    def __init__(self, study_strategy_param: StudyStrategyParam | None) -> None:
        super().__init__(study_strategy_param)
        self.found_mapping: Mapping | None = None

    def is_done(
        self,
        trial_table: TrialTable,  # noqa: ARG002
        parameter_space: ParameterAlignedSpace,  # noqa: ARG002
        trial_repository: BaseTrialRepository,
    ) -> bool:
        if self.found_mapping:
            return True
        self.found_mapping = self._find(trial_repository)
        return bool(self.found_mapping)

    def _find(self, trial_repository: BaseTrialRepository) -> Mapping | None:
        trials = trial_repository.load_all()
        for trial in trials:
            finding = Trial.from_model(trial).find_target_value(self.study_strategy_param.target_value)
            if finding:
                return finding
        return None

    def extract_mappings(self, trial_repository: BaseTrialRepository) -> MappingsStorage:
        if not self.found_mapping:
            self.found_mapping = self._find(trial_repository)
        if not self.found_mapping:
            raise LD2NotDoneError

        params = tuple(param.to_dummy() for param in self.found_mapping.params)
        result = self.found_mapping.result.to_dummy()

        return MappingsStorage(params_info=params, result_info=result, values=[self.found_mapping.to_tuple()])

    def to_model(self) -> StudyStrategyModel:
        return StudyStrategyModel(
            type="find_exact",
            study_strategy_param=self.study_strategy_param,
        )
