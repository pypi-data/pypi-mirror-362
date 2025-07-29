from datetime import datetime

import pytest

from lite_dist2.curriculum_models.progress_summary import (
    ReportMaterial,
    StudyProgressSummary,
    WorkerEfficiency,
    report_study_progress,
)
from lite_dist2.curriculum_models.trial import TrialDoneRecord
from tests.const import JST

NOW = datetime(2025, 6, 28, 19, 45, 0, tzinfo=JST)


@pytest.mark.parametrize(
    ("report_material", "expected"),
    [
        pytest.param(
            ReportMaterial(
                study_id="s01",
                study_name="s01",
                records=[
                    TrialDoneRecord(
                        trial_id="t01",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 40, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 42, 0, tzinfo=JST),
                        worker_node_id="w01",
                        worker_node_name="w01",
                        grid_size=100,
                    ),
                    TrialDoneRecord(
                        trial_id="t02",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 42, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 44, 0, tzinfo=JST),
                        worker_node_id="w01",
                        worker_node_name="w01",
                        grid_size=100,
                    ),
                ],
                total_grid=None,
                done_grid=400,
            ),
            StudyProgressSummary(
                study_id="s01",
                study_name="s01",
                total_grid="infinite",
                done_grid=400,
                grid_velocity=0.4,
                eta="unpredictable",
                worker_efficiencies=[
                    WorkerEfficiency(worker_id="w01", worker_name="w01", grid_velocity=0.4),
                ],
            ),
            id="Infinite space",
        ),
        pytest.param(
            ReportMaterial(
                study_id="s01",
                study_name="s01",
                records=[],
                total_grid=1000,
                done_grid=400,
            ),
            StudyProgressSummary(
                study_id="s01",
                study_name="s01",
                total_grid=1000,
                done_grid=400,
                grid_velocity=0,
                eta="unpredictable",
                worker_efficiencies=[],
            ),
            id="Stopped study",
        ),
        pytest.param(
            ReportMaterial(
                study_id="s01",
                study_name="s01",
                records=[
                    TrialDoneRecord(
                        trial_id="t01",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 40, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 42, 0, tzinfo=JST),
                        worker_node_id="w01",
                        worker_node_name="w01",
                        grid_size=100,
                    ),
                    TrialDoneRecord(
                        trial_id="t03",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 41, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 43, 0, tzinfo=JST),
                        worker_node_id="w02",
                        worker_node_name="w02",
                        grid_size=50,
                    ),
                    TrialDoneRecord(
                        trial_id="t02",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 42, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 44, 0, tzinfo=JST),
                        worker_node_id="w01",
                        worker_node_name="w01",
                        grid_size=100,
                    ),
                    TrialDoneRecord(
                        trial_id="t04",
                        reserved_timestamp=datetime(2025, 6, 28, 19, 43, 0, tzinfo=JST),
                        registered_timestamp=datetime(2025, 6, 28, 19, 45, 0, tzinfo=JST),
                        worker_node_id="w02",
                        worker_node_name="w02",
                        grid_size=50,
                    ),
                ],
                total_grid=1000,
                done_grid=400,
            ),
            StudyProgressSummary(
                study_id="s01",
                study_name="s01",
                total_grid=1000,
                done_grid=400,
                grid_velocity=0.6,
                eta=datetime(2025, 6, 28, 20, 1, 40, tzinfo=JST),
                worker_efficiencies=[
                    WorkerEfficiency(worker_id="w01", worker_name="w01", grid_velocity=0.4),
                    WorkerEfficiency(worker_id="w02", worker_name="w02", grid_velocity=0.2),
                ],
            ),
            id="Normal double worker",
        ),
    ],
)
def test_report_study_progress(
    report_material: ReportMaterial,
    expected: StudyProgressSummary,
) -> None:
    cutoff_sec = 500
    actual = report_study_progress(NOW, cutoff_sec, report_material)
    assert actual.study_id == expected.study_id
    assert actual.study_name == expected.study_name
    assert actual.total_grid == expected.total_grid
    assert actual.done_grid == expected.done_grid
    assert actual.grid_velocity == pytest.approx(expected.grid_velocity)
    assert actual.eta == expected.eta
    assert actual.worker_efficiencies == expected.worker_efficiencies
