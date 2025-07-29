from __future__ import annotations

from typing import TYPE_CHECKING

from lite_dist2.expections import LD2ModelTypeError
from lite_dist2.study_strategies.all_calculation_study_strategy import AllCalculationStudyStrategy
from lite_dist2.study_strategies.find_exact_study_strategy import FindExactStudyStrategy

if TYPE_CHECKING:
    from lite_dist2.study_strategies import BaseStudyStrategy, StudyStrategyModel


def create_study_strategy(model: StudyStrategyModel) -> BaseStudyStrategy:
    match model.type:
        case "all_calculation":
            return AllCalculationStudyStrategy(model.study_strategy_param)
        case "find_exact":
            return FindExactStudyStrategy(model.study_strategy_param)
        case "minimize":
            raise NotImplementedError
        case _:
            raise LD2ModelTypeError(model.type)
