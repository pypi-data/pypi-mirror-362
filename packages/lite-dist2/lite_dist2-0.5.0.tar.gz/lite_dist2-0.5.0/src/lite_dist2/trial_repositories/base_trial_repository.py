import abc
from pathlib import Path

from lite_dist2.curriculum_models.trial import TrialModel
from lite_dist2.trial_repositories.trial_repository_model import TrialRepositoryModel
from lite_dist2.type_definitions import TrialRepositoryType


class BaseTrialRepository(abc.ABC):
    def __init__(self, save_dir: Path) -> None:
        self.save_dir = save_dir

    @staticmethod
    @abc.abstractmethod
    def get_repository_type() -> TrialRepositoryType:
        pass

    @abc.abstractmethod
    def clean_save_dir(self) -> None:
        pass

    @abc.abstractmethod
    def save(self, trial: TrialModel) -> None:
        pass

    @abc.abstractmethod
    def load(self, trial_id: str) -> TrialModel:
        pass

    @abc.abstractmethod
    def load_all(self) -> list[TrialModel]:
        pass

    @abc.abstractmethod
    def delete_save_dir(self) -> None:
        pass

    def to_model(self) -> TrialRepositoryModel:
        return TrialRepositoryModel(type=self.get_repository_type(), save_dir=self.save_dir)
