from __future__ import annotations

from pydantic import BaseModel, Field

from lite_dist2.curriculum_models.study_portables import StudyRegistry
from lite_dist2.curriculum_models.trial import TrialModel


class BaseParam(BaseModel):
    pass


class StudyRegisterParam(BaseParam):
    study: StudyRegistry = Field(
        ...,
        description="`Study` to register",
    )


class TrialReserveParam(BaseParam):
    retaining_capacity: set[str] = Field(
        ...,
        description="List of capabilities that the worker node has.",
    )
    max_size: int = Field(
        ...,
        description="The maximum size of parameter space reserving.",
    )
    worker_node_name: str | None = Field(
        default=None,
        description="Name of the worker node. ",
    )
    worker_node_id: str = Field(
        ...,
        description="ID of the worker node",
    )


class TrialRegisterParam(BaseModel):
    trial: TrialModel = Field(
        ...,
        description="Registering trial to the table node.",
    )
