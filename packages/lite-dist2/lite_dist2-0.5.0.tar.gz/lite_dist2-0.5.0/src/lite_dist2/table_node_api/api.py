from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Annotated

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from lite_dist2.curriculum_models.curriculum import CurriculumProvider
from lite_dist2.curriculum_models.study import Study
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.curriculum_models.trial import Trial
from lite_dist2.expections import LD2ParameterError
from lite_dist2.table_node_api.table_param import StudyRegisterParam, TrialRegisterParam, TrialReserveParam
from lite_dist2.table_node_api.table_response import (
    CurriculumSummaryResponse,
    OkResponse,
    ProgressSummaryResponse,
    StudyRegisteredResponse,
    StudyResponse,
    TrialReserveResponse,
)

if TYPE_CHECKING:
    from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


def _response(model: BaseModel, status_code: int) -> JSONResponse:
    return JSONResponse(content=model.model_dump(mode="json"), status_code=status_code)


@app.get("/ping")
def handle_ping() -> OkResponse:
    return OkResponse(ok=True)


@app.get("/save")
def handle_save() -> OkResponse:
    curr = CurriculumProvider.get()
    curr.save()
    return OkResponse(ok=True)


@app.get("/status", response_model=CurriculumSummaryResponse)
def handle_status() -> CurriculumSummaryResponse | JSONResponse:
    curr = CurriculumProvider.get()
    return _response(CurriculumSummaryResponse(summaries=curr.to_summaries()), 200)


@app.get("/status/progress", response_model=ProgressSummaryResponse)
def handle_status_progress(
    cutoff_sec: Annotated[int, Query(description="Time range of Trial used for ETA estimation.")] = 600,
) -> ProgressSummaryResponse | JSONResponse:
    curr = CurriculumProvider.get()
    return _response(curr.report_progress(cutoff_sec), 200)


@app.post("/study/register", response_model=StudyRegisteredResponse)
def handle_study_register(
    study_registry: Annotated[StudyRegisterParam, Body(description="Registry of processing study")],
) -> StudyRegisteredResponse | JSONResponse:
    if not study_registry.study.is_valid():
        raise HTTPException(status_code=400, detail="Cannot use together infinite space and all_calculation strategy.")

    curr = CurriculumProvider.get()
    new_study = Study.from_model(study_registry.study.to_study_model(curr.trial_file_dir))

    if curr.try_insert_study(new_study):
        new_study.trial_repo.clean_save_dir()
        return _response(StudyRegisteredResponse(study_id=new_study.study_id), 200)
    raise HTTPException(status_code=400, detail=f'The name("{new_study.name}") of study is already registered.')


@app.post("/trial/reserve", response_model=TrialReserveResponse)
def handle_trial_reserve(
    param: Annotated[TrialReserveParam, Body(description="Reserved trial parameter")],
) -> TrialReserveResponse | JSONResponse:
    curr = CurriculumProvider.get()
    study = curr.get_available_study(param.retaining_capacity)
    if study is None:
        return _response(TrialReserveResponse(trial=None), 202)

    trial = study.suggest_next_trial(param.max_size, param.worker_node_name, param.worker_node_id)
    if trial is None:
        return _response(TrialReserveResponse(trial=None), 202)
    return _response(TrialReserveResponse(trial=trial.to_model()), 200)


@app.post("/trial/register", response_model=OkResponse)
def handle_trial_register(
    param: Annotated[TrialRegisterParam, Body(description="Registering trial")],
) -> OkResponse | JSONResponse:
    curr = CurriculumProvider.get()
    trial = param.trial
    study = curr.find_study_by_id(trial.study_id)
    if study is None:
        raise HTTPException(status_code=404, detail=f"Study not found: study_id={trial.study_id}")

    try:
        study.receipt_trial(Trial.from_model(trial))
    except LD2ParameterError:
        return _response(OkResponse(ok=False), 409)
    curr.to_storage_if_done()
    return _response(OkResponse(ok=True), 200)


@app.get("/study", response_model=StudyResponse)
def handle_study(
    study_id: Annotated[str | None, Query(description="`study_id` of the target study")] = None,
    name: Annotated[str | None, Query(description="`name` of the target study")] = None,
) -> StudyResponse | JSONResponse:
    if study_id is None and name is None:
        raise HTTPException(status_code=400, detail="One of study_id or name should be set.")
    if study_id is not None and name is not None:
        raise HTTPException(status_code=400, detail="Only one of study_id or name should be set.")

    curr = CurriculumProvider.get()
    storage = curr.pop_storage(study_id, name)
    if storage is not None:
        storage.consume_trial()
        return _response(StudyResponse(status=StudyStatus.done, result=storage), 200)

    # 見つからなかったか、終わってない
    study_status = curr.get_study_status(study_id, name)
    resp = StudyResponse(status=study_status, result=None)
    if study_status == StudyStatus.not_found:
        return _response(resp, status_code=404)
    return _response(resp, 202)


@app.delete("/study", response_model=OkResponse)
def handle_study_cancel(
    study_id: Annotated[str | None, Query(description="`study_id` of the target study")] = None,
    name: Annotated[str | None, Query(description="`name` of the target study")] = None,
) -> OkResponse | JSONResponse:
    if study_id is None and name is None:
        raise HTTPException(status_code=400, detail="One of study_id or name should be set.")
    if study_id is not None and name is not None:
        raise HTTPException(status_code=400, detail="Only one of study_id or name should be set.")

    curr = CurriculumProvider.get()
    try:
        found_and_cancel = curr.cancel_study(study_id, name)
    except LD2ParameterError:
        return _response(OkResponse(ok=False), 400)

    if found_and_cancel:
        return _response(OkResponse(ok=True), 200)
    return _response(OkResponse(ok=False), 404)
