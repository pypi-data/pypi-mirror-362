from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests

from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.curriculum_models.trial import Trial
from lite_dist2.expections import LD2TableNodeServerError
from lite_dist2.table_node_api.table_param import StudyRegisterParam, TrialRegisterParam, TrialReserveParam
from lite_dist2.table_node_api.table_response import (
    OkResponse,
    StudyRegisteredResponse,
    StudyResponse,
    TrialReserveResponse,
)

if TYPE_CHECKING:
    from typing import Any, ClassVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableNodeClient:
    INSTANT_API_TIMEOUT_SECONDS = 10
    HEADERS: ClassVar[dict[str, str]] = {"Content-Type": "application/json; charset=utf-8"}

    def __init__(self, ip: str, port: int | str) -> None:
        self.domain = f"http://{ip}:{port}"

    def ping(self) -> bool:
        try:
            _ = self._get("/ping", timeout=self.INSTANT_API_TIMEOUT_SECONDS)
        except LD2TableNodeServerError:
            return False
        return True

    def register_study(self, param: StudyRegisterParam) -> StudyRegisteredResponse:
        _, d = self._post("/study/register", self.INSTANT_API_TIMEOUT_SECONDS, param.model_dump(mode="json"))

        resp = StudyRegisteredResponse.model_validate(d)
        logger.info("Registered study: %s", resp.study_id)
        return resp

    def reserve_trial(
        self,
        worker_id: str,
        worker_name: str | None,
        max_size: int,
        retaining_capacity: set[str],
        timeout_seconds: int,
    ) -> Trial | None:
        param = TrialReserveParam(
            retaining_capacity=retaining_capacity,
            max_size=max_size,
            worker_node_name=worker_name,
            worker_node_id=worker_id,
        )
        status_code, d = self._post("/trial/reserve", timeout_seconds, param.model_dump(mode="json"))

        resp = TrialReserveResponse.model_validate(d)
        if status_code == requests.codes.accepted or resp.trial is None:
            logger.info("Cannot reserve trial")
            return None

        trial = Trial.from_model(resp.trial)
        logger.info("Reserved trial (size=%d)", trial.parameter_space.get_total())
        return trial

    def register_trial(self, trial: Trial, timeout_seconds: int) -> None:
        param = TrialRegisterParam(trial=trial.to_model())
        status_code, _ = self._post("/trial/register", timeout_seconds, param.model_dump(mode="json"))
        if status_code == requests.codes.conflict:
            logger.warning("Failed to register trial. This trial might be timed out or study might be cancelled.")
        elif status_code != requests.codes.ok:
            logger.warning("Failed to register trial.")

    def study(self, study_id: str | None = None, name: str | None = None) -> StudyResponse | None:
        _, resp = self._get("/study", self.INSTANT_API_TIMEOUT_SECONDS, {"study_id": study_id, "name": name})
        study_response = StudyResponse.model_validate(resp)
        if study_response.status != StudyStatus.done:
            detail_info = f"{study_id=}" if study_id is not None else f"{name=}"
            logger.info("Study(%s) is %s", detail_info, str(study_response))
        return study_response

    def save(self) -> OkResponse:
        _, resp = self._get("/save", self.INSTANT_API_TIMEOUT_SECONDS)
        return OkResponse.model_validate(resp)

    def _get(self, path: str, timeout: int, query: dict[str, str] | None = None) -> tuple[int, dict[str, Any]]:
        url = f"{self.domain}{path}"
        response = requests.get(
            url,
            headers=self.HEADERS,
            params=query,
            timeout=timeout,
        )
        return response.status_code, response.json()

    def _post(self, path: str, timeout_seconds: int, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        url = f"{self.domain}{path}"
        response = requests.post(
            url,
            headers=self.HEADERS,
            json=body,
            timeout=timeout_seconds,
        )
        return response.status_code, response.json()
