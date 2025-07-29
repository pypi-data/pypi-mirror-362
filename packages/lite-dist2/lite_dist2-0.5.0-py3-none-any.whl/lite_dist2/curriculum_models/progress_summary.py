from collections import defaultdict
from datetime import datetime, timedelta
from typing import Literal

from pydantic import BaseModel

from lite_dist2.curriculum_models.trial import TrialDoneRecord


class WorkerEfficiency(BaseModel):
    worker_id: str
    worker_name: str | None
    grid_velocity: float


class StudyProgressSummary(BaseModel):
    study_id: str
    study_name: str | None
    total_grid: int | Literal["infinite"]
    done_grid: int
    grid_velocity: float
    eta: datetime | Literal["unpredictable"]
    worker_efficiencies: list[WorkerEfficiency]


class ReportMaterial(BaseModel):
    study_id: str
    study_name: str | None
    records: list[TrialDoneRecord]
    total_grid: int | None
    done_grid: int


def report_study_progress(
    now: datetime,
    cutoff_sec: int,
    report_material: ReportMaterial,
) -> StudyProgressSummary:
    records_worker_map = defaultdict(list)
    for rec in report_material.records:
        records_worker_map[rec.worker_node_id].append(rec)

    records_worker_map = dict(records_worker_map)
    worker_efficiencies = []
    for wni, worker_records in records_worker_map.items():
        if not worker_records:
            continue
        worker_efficiencies.append(
            WorkerEfficiency(
                worker_id=wni,
                worker_name=worker_records[0].worker_node_name,
                grid_velocity=sum(rec.grid_size for rec in worker_records) / cutoff_sec,
            ),
        )
    worker_efficiencies = sorted(worker_efficiencies, key=lambda e: e.grid_velocity, reverse=True)
    total_grid_velocity = sum(e.grid_velocity for e in worker_efficiencies)

    if report_material.total_grid is None:
        return StudyProgressSummary(
            study_id=report_material.study_id,
            study_name=report_material.study_name,
            total_grid="infinite",
            done_grid=report_material.done_grid,
            grid_velocity=total_grid_velocity,
            eta="unpredictable",
            worker_efficiencies=worker_efficiencies,
        )
    if total_grid_velocity == 0:
        return StudyProgressSummary(
            study_id=report_material.study_id,
            study_name=report_material.study_name,
            total_grid=report_material.total_grid,
            done_grid=report_material.done_grid,
            grid_velocity=0,
            eta="unpredictable",
            worker_efficiencies=worker_efficiencies,
        )

    eta_sec = (report_material.total_grid - report_material.done_grid) / total_grid_velocity
    return StudyProgressSummary(
        study_id=report_material.study_id,
        study_name=report_material.study_name,
        total_grid=report_material.total_grid,
        done_grid=report_material.done_grid,
        grid_velocity=total_grid_velocity,
        eta=now + timedelta(seconds=eta_sec),
        worker_efficiencies=worker_efficiencies,
    )
