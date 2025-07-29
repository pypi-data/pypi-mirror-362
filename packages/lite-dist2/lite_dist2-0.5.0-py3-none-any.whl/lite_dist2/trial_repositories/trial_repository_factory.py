from __future__ import annotations

from typing import TYPE_CHECKING

from lite_dist2.expections import LD2UndefinedError
from lite_dist2.trial_repositories.normal_trial_repository import NormalTrialRepository

if TYPE_CHECKING:
    from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
    from lite_dist2.trial_repositories.trial_repository_model import TrialRepositoryModel


def create_trial_repository(model: TrialRepositoryModel) -> BaseTrialRepository:
    match model.type:
        case "normal":
            return NormalTrialRepository.from_model(model)
        case _:
            raise LD2UndefinedError(model.type)
