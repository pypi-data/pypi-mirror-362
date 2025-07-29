from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from lite_dist2.curriculum_models.progress_summary import StudyProgressSummary
from lite_dist2.curriculum_models.study_portables import StudyStorage, StudySummary
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.curriculum_models.trial import TrialModel


class BaseTableResponse(BaseModel):
    pass


class OkResponse(BaseTableResponse):
    ok: bool = Field(...)


class TrialReserveResponse(BaseTableResponse):
    trial: TrialModel | None = Field(
        ...,
        description=(
            "Reserved trial for the worker node. "
            "None if the curriculum is empty or no trial which can be processed by the worker node's capabilities."
        ),
    )


class StudyRegisteredResponse(BaseTableResponse):
    study_id: str = Field(
        ...,
        description="Published `study_id` of registered study.",
    )


class StudyResponse(BaseTableResponse):
    status: StudyStatus = Field(
        ...,
        description="Status of the target Study.",
    )
    result: StudyStorage | None = Field(
        None,
        description="Results of completed study. If the study is not completed or not found, then `None`.",
    )


class CurriculumSummaryResponse(BaseTableResponse):
    summaries: list[StudySummary] = Field(
        ...,
        description="The list of study (containing storage) summary.",
    )


class ProgressSummaryResponse(BaseModel):
    now: datetime
    cutoff_sec: int
    progress_summaries: list[StudyProgressSummary]
