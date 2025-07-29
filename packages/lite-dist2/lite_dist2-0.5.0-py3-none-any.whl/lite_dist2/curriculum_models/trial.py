from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from lite_dist2.common import publish_timestamp
from lite_dist2.curriculum_models.mapping import Mapping
from lite_dist2.expections import LD2ModelTypeError, LD2NotDoneError, LD2UndefinedError
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.const_param import ConstParam
from lite_dist2.value_models.jagged_space import ParameterJaggedSpace, ParameterJaggedSpaceModel
from lite_dist2.value_models.point import ResultType, ScalarValue, VectorValue

if TYPE_CHECKING:
    from lite_dist2.type_definitions import RawParamType, RawResultType
    from lite_dist2.value_models.base_space import FlattenSegment, ParameterSpace


class TrialStatus(str, Enum):
    running = "running"
    done = "done"


class TrialDoneRecord(BaseModel):
    trial_id: str
    reserved_timestamp: datetime
    worker_node_name: str | None
    worker_node_id: str
    registered_timestamp: datetime
    grid_size: int

    def calc_duration_sec(self) -> float:
        dt = self.registered_timestamp - self.reserved_timestamp
        return dt.total_seconds()

    def calc_grid_per_sec(self) -> float:
        return self.grid_size / self.calc_duration_sec()


class TrialModel(BaseModel):
    study_id: str
    trial_id: str
    reserved_timestamp: datetime
    trial_status: TrialStatus
    const_param: ConstParam | None
    parameter_space: ParameterAlignedSpaceModel | ParameterJaggedSpaceModel
    result_type: Literal["scalar", "vector"]
    result_value_type: Literal["bool", "int", "float"]
    worker_node_name: str | None
    worker_node_id: str
    results: list[Mapping] | None = None
    registered_timestamp: datetime | None = None


class Trial:
    def __init__(
        self,
        study_id: str,
        trial_id: str,
        reserved_timestamp: datetime,
        trial_status: TrialStatus,
        const_param: ConstParam | None,
        parameter_space: ParameterSpace,
        result_type: Literal["scalar", "vector"],
        result_value_type: Literal["bool", "int", "float"],
        worker_node_name: str | None,
        worker_node_id: str,
        results: list[Mapping] | None = None,
        registered_timestamp: datetime | None = None,
    ) -> None:
        self.study_id = study_id
        self.trial_id = trial_id
        self.reserved_timestamp = reserved_timestamp
        self.trial_status = trial_status
        self.const_param = const_param
        self.parameter_space = parameter_space
        self.result_type = result_type
        self.result_value_type = result_value_type
        self.worker_node_name = worker_node_name
        self.worker_node_id = worker_node_id
        self.result = results
        self.registered_timestamp = registered_timestamp

    def convert_mappings_from(self, raw_mappings: list[tuple[RawParamType, RawResultType]]) -> list[Mapping]:
        mappings = []
        for raw_param, raw_res in raw_mappings:
            param = self.parameter_space.value_tuple_to_param_type(raw_param)
            result = self._create_result_value(raw_res)
            mappings.append(Mapping(params=param, result=result))
        return mappings

    def set_result(self, mappings: list[Mapping]) -> None:
        self.result = mappings

    def set_registered_timestamp(self) -> None:
        self.registered_timestamp = publish_timestamp()

    def get_running_segments(self) -> list[FlattenSegment]:
        if self.trial_status == TrialStatus.running:
            return self.parameter_space.get_flatten_ambient_start_and_size_list()
        return []

    def _create_result_value(self, raw_result: RawResultType) -> ResultType:
        match self.result_type:
            case "scalar":
                return ScalarValue.create_from_numeric(raw_result, self.result_value_type)
            case "vector":
                return VectorValue.create_from_numeric(raw_result, self.result_value_type)
            case _:
                raise LD2ModelTypeError(self.result_type)

    def measure_seconds_from_registered(self, now: datetime) -> int:
        delta = now - self.reserved_timestamp
        return int(delta.total_seconds())

    def find_target_value(self, target_value: ResultType) -> Mapping | None:
        # find_exact 用
        if not self.result:
            return None
        if self.trial_status != TrialStatus.done:
            return None

        for mapping in self.result:
            if mapping.result.equal_to(target_value):
                return mapping
        return None

    def to_done_record(self) -> TrialDoneRecord:
        if self.trial_status != TrialStatus.done or self.registered_timestamp is None:
            raise LD2NotDoneError

        return TrialDoneRecord(
            trial_id=self.trial_id,
            reserved_timestamp=self.reserved_timestamp,
            worker_node_name=self.worker_node_name,
            worker_node_id=self.worker_node_id,
            registered_timestamp=self.registered_timestamp,
            grid_size=self.parameter_space.get_total(),
        )

    def done_in_after(self, cutoff_datetime: datetime) -> bool:
        if self.trial_status != TrialStatus.done or self.registered_timestamp is None:
            return False
        return cutoff_datetime < self.registered_timestamp

    def to_model(self) -> TrialModel:
        return TrialModel(
            study_id=self.study_id,
            trial_id=self.trial_id,
            reserved_timestamp=self.reserved_timestamp,
            trial_status=self.trial_status,
            const_param=self.const_param,
            parameter_space=self.parameter_space.to_model(),
            result_type=self.result_type,
            result_value_type=self.result_value_type,
            worker_node_name=self.worker_node_name,
            worker_node_id=self.worker_node_id,
            results=self.result,
            registered_timestamp=self.registered_timestamp,
        )

    @staticmethod
    def from_model(model: TrialModel) -> Trial:
        match model.parameter_space.type:
            case "aligned":
                parameter_space = ParameterAlignedSpace.from_model(model.parameter_space)
            case "jagged":
                parameter_space = ParameterJaggedSpace.from_model(model.parameter_space)
            case _:
                raise LD2UndefinedError(model.parameter_space.type)
        return Trial(
            study_id=model.study_id,
            trial_id=model.trial_id,
            reserved_timestamp=model.reserved_timestamp,
            trial_status=model.trial_status,
            const_param=model.const_param,
            parameter_space=parameter_space,
            result_type=model.result_type,
            result_value_type=model.result_value_type,
            worker_node_name=model.worker_node_name,
            worker_node_id=model.worker_node_id,
            results=model.results,
            registered_timestamp=model.registered_timestamp,
        )
