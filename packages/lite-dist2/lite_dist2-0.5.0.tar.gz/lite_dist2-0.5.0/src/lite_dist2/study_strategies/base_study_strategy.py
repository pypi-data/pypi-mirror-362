from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from lite_dist2.value_models.point import ResultType

if TYPE_CHECKING:
    from lite_dist2.curriculum_models.mapping import MappingsStorage
    from lite_dist2.curriculum_models.trial_table import TrialTable
    from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
    from lite_dist2.value_models.aligned_space import ParameterAlignedSpace


class StudyStrategyParam(BaseModel):
    target_value: ResultType


class StudyStrategyModel(BaseModel):
    type: Literal["all_calculation", "find_exact", "minimize"]
    study_strategy_param: StudyStrategyParam | None


class BaseStudyStrategy(metaclass=abc.ABCMeta):
    def __init__(self, study_strategy_param: StudyStrategyParam | None) -> None:
        self.study_strategy_param = study_strategy_param

    @abc.abstractmethod
    def is_done(
        self,
        trial_table: TrialTable,
        parameter_space: ParameterAlignedSpace,
        trial_repository: BaseTrialRepository,
    ) -> bool:
        pass

    @abc.abstractmethod
    def extract_mappings(self, trial_repository: BaseTrialRepository) -> MappingsStorage:
        pass

    @abc.abstractmethod
    def to_model(self) -> StudyStrategyModel:
        pass
