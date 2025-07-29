from __future__ import annotations

import json
import shutil
from typing import TYPE_CHECKING

from lite_dist2.curriculum_models.trial import TrialModel
from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository

if TYPE_CHECKING:
    from lite_dist2.trial_repositories.trial_repository_model import TrialRepositoryModel
    from lite_dist2.type_definitions import TrialRepositoryType


class NormalTrialRepository(BaseTrialRepository):
    @staticmethod
    def get_repository_type() -> TrialRepositoryType:
        return "normal"

    def clean_save_dir(self) -> None:
        if self.save_dir.exists():
            for item in self.save_dir.iterdir():
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        else:
            self.save_dir.mkdir(parents=True, exist_ok=True)

    def save(self, trial_model: TrialModel) -> None:
        path = self.save_dir / f"{trial_model.trial_id}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(trial_model.model_dump(mode="json"), f, ensure_ascii=False)

    def load(self, trial_id: str) -> TrialModel:
        path = self.save_dir / f"{trial_id}.json"
        with path.open("r", encoding="utf-8") as f:
            d = json.load(f)
        return TrialModel.model_validate(d)

    def load_all(self) -> list[TrialModel]:
        trials = []
        if not self.save_dir.exists() or not self.save_dir.is_dir():
            raise FileNotFoundError(self.save_dir)

        for json_path in self.save_dir.glob("*.json"):
            with json_path.open("r", encoding="utf-8") as f:
                d = json.load(f)
                trials.append(TrialModel.model_validate(d))
        return trials

    def delete_save_dir(self) -> None:
        if self.save_dir.exists():
            shutil.rmtree(self.save_dir)

    @staticmethod
    def from_model(model: TrialRepositoryModel) -> NormalTrialRepository:
        return NormalTrialRepository(model.save_dir)
