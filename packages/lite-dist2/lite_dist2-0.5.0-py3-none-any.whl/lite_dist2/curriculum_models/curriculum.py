from __future__ import annotations

import json
import logging
import threading
import time
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel

from lite_dist2.common import publish_timestamp
from lite_dist2.config import TableConfigProvider
from lite_dist2.curriculum_models.progress_summary import ReportMaterial, report_study_progress
from lite_dist2.curriculum_models.study import Study
from lite_dist2.curriculum_models.study_portables import StudyModel, StudyStorage, StudySummary
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.expections import LD2ParameterError
from lite_dist2.table_node_api.table_response import ProgressSummaryResponse

if TYPE_CHECKING:
    import pathlib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CurriculumModel(BaseModel):
    studies: list[StudyModel]
    storages: list[StudyStorage]
    trial_file_dir: Path


class Curriculum:
    def __init__(self, studies: list[Study], storages: list[StudyStorage], trial_file_dir: Path) -> None:
        self.studies = studies
        self.storages = storages
        self.trial_file_dir = trial_file_dir
        self._lock = threading.Lock()

    def get_available_study(self, retaining_capacity: set[str]) -> Study | None:
        with self._lock:
            for study in self.studies:
                if study.status == StudyStatus.running and study.required_capacity.issubset(retaining_capacity):
                    return study
            for study in self.studies:
                if study.status == StudyStatus.wait and study.required_capacity.issubset(retaining_capacity):
                    return study
        return None

    def find_study_by_id(self, study_id: str) -> Study | None:
        with self._lock:
            for study in self.studies:
                if study.study_id == study_id:
                    return study
        return None

    def try_insert_study(self, study: Study) -> bool:
        with self._lock:
            study_names = {st.name for st in self.studies if st.name is not None}
            storage_names = {st.name for st in self.storages if st.name is not None}
            if study.name is not None and (study.name in study_names or study.name in storage_names):
                return False

            self.studies.append(study)
        return True

    def to_storage_if_done(self) -> None:
        with self._lock:
            self.studies = [study for study in self.studies if not self._move_to_storage_if_done(study)]

    def _move_to_storage_if_done(self, study: Study) -> bool:
        study.update_status()
        if study.is_done():
            self.storages.append(study.to_storage())
            return True
        return False

    def pop_storage(self, study_id: str | None, name: str | None) -> StudyStorage | None:
        storages = []
        target = None
        if study_id is not None:
            for storage in self.storages:
                if storage.study_id == study_id:
                    target = storage
                    continue
                storages.append(storage)
            self.storages = storages
            return target

        if name is not None:
            for storage in self.storages:
                if storage.name == name:
                    target = storage
                    continue
                storages.append(storage)
            self.storages = storages
            return target
        p = "study_id, name"
        e = "Both are None"
        raise LD2ParameterError(p, e)

    def get_study_status(self, study_id: str | None, name: str | None) -> StudyStatus:
        if study_id is not None:
            return self._get_study_status_by_id(study_id)

        if name is not None:
            return self._get_study_status_by_name(name)

        p = "study_id, name"
        e = "Both are None"
        raise LD2ParameterError(p, e)

    def report_progress(self, cutoff_sec: int) -> ProgressSummaryResponse:
        now = publish_timestamp()
        cutoff_datetime = now - timedelta(seconds=cutoff_sec)

        with self._lock:
            report_materials = [
                ReportMaterial(
                    study_id=study.study_id,
                    study_name=study.name,
                    records=study.trial_table.gen_done_record_list(max(cutoff_datetime, study.registered_timestamp)),
                    total_grid=study.parameter_space.get_total(),
                    done_grid=study.trial_table.count_grid(),
                )
                for study in self.studies
            ]
        return ProgressSummaryResponse(
            now=now,
            cutoff_sec=cutoff_sec,
            progress_summaries=[report_study_progress(now, cutoff_sec, material) for material in report_materials],
        )

    def _get_study_status_by_id(self, study_id: str) -> StudyStatus:
        for study in self.studies:
            if study.study_id == study_id:
                return study.status
        for storage in self.storages:
            if storage.study_id == study_id:
                return StudyStatus.done
        return StudyStatus.not_found

    def _get_study_status_by_name(self, name: str) -> StudyStatus:
        for study in self.studies:
            if study.name == name:
                return study.status
        for storage in self.storages:
            if storage.name == name:
                return StudyStatus.done
        return StudyStatus.not_found

    def check_timeout_trial(self) -> None:
        removed_ids = []
        timeout_seconds = TableConfigProvider.get().trial_timeout_seconds
        for study in self.studies:
            removed_ids.extend(study.check_timeout_trial(publish_timestamp(), timeout_seconds))
        if len(removed_ids) > 0:
            logger.info("Outdated trials: %s", ", ".join(removed_ids))
        else:
            logger.info("No trials are outdated")

    def to_model(self) -> CurriculumModel:
        return CurriculumModel(
            studies=[study.to_model() for study in self.studies],
            storages=self.storages,
            trial_file_dir=self.trial_file_dir,
        )

    def to_summaries(self) -> list[StudySummary]:
        return [storage.to_summary() for storage in self.storages] + [study.to_summary() for study in self.studies]

    @staticmethod
    def from_model(model: CurriculumModel) -> Curriculum:
        return Curriculum(
            studies=[Study.from_model(study) for study in model.studies],
            storages=model.storages,
            trial_file_dir=model.trial_file_dir,
        )

    def save(self, curr_json_path: pathlib.Path | None = None) -> None:
        save_start_time = time.perf_counter()
        if curr_json_path is None:
            curr_json_path = TableConfigProvider.get().curriculum_path

        model = self.to_model()
        with curr_json_path.open("w", encoding="utf-8") as f:
            json.dump(model.model_dump(mode="json"), f, ensure_ascii=False)
        save_end_time = time.perf_counter()
        logger.info("Saved curriculum in %.3f msec", (save_end_time - save_start_time) * 1000)

    def cancel_study(self, study_id: str | None, name: str | None) -> bool:
        studies = []
        found = False
        if study_id is not None:
            with self._lock:
                for study in self.studies:
                    if study.study_id == study_id:
                        found = True
                        continue
                    studies.append(study)
                self.studies = studies
            return found

        if name is not None:
            with self._lock:
                for study in self.studies:
                    if study.name == name:
                        found = True
                        continue
                    studies.append(study)
                self.studies = studies
            return found
        p = "study_id, name"
        e = "Both are None"
        raise LD2ParameterError(p, e)

    @staticmethod
    def load_or_create(curr_json_path: pathlib.Path | None = None) -> Curriculum:
        load_start_time = time.perf_counter()
        if curr_json_path is None:
            curr_json_path = TableConfigProvider.get().curriculum_path

        if curr_json_path.exists():
            with curr_json_path.open("r", encoding="utf-8") as f:
                json_dict = json.load(f)
            model = CurriculumModel.model_validate(json_dict)
            return Curriculum.from_model(model)
        load_end_time = time.perf_counter()
        logger.info("Loaded curriculum in %.3f msec", (load_end_time - load_start_time) * 1000)
        return Curriculum([], [], TableConfigProvider.get().trial_file_dir)


class CurriculumProvider:
    _CURR: Curriculum | None = None

    @classmethod
    def get(cls) -> Curriculum:
        if cls._CURR is not None:
            return cls._CURR
        cls._CURR = Curriculum.load_or_create()
        return cls._CURR

    @classmethod
    async def save_async(cls) -> None:
        if cls._CURR is None:
            return
        cls._CURR.save()

    @classmethod
    async def check_timeout(cls) -> None:
        if cls._CURR is None:
            return
        cls._CURR.check_timeout_trial()
