from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from lite_dist2.type_definitions import PortableValueType
from lite_dist2.value_models.point import ParamType, ResultType

if TYPE_CHECKING:
    from typing import Literal


class Mapping(BaseModel):
    params: ParamType
    result: ResultType

    def to_tuple(self) -> tuple[PortableValueType, ...]:
        values = [param.value for param in self.params]
        values.extend(self.result.get_value_list())
        return tuple(values)


class MappingsStorage(BaseModel):
    params_info: ParamType
    result_info: ResultType
    values: list[tuple[PortableValueType, ...]]

    def get_names(self) -> tuple[str | None, ...]:
        names = [param.name for param in self.params_info]
        names.append(self.result_info.name)
        return tuple(names)

    def are_results(self) -> tuple[bool, ...]:
        p_size = len(self.params_info)
        r_size = self.result_info.get_value_size()
        return tuple([False] * p_size + [True] * r_size)

    def get_types(self) -> tuple[Literal["bool", "int", "float"], ...]:
        types = [param.value_type for param in self.params_info]
        types.extend(self.result_info.get_value_types())
        return tuple(types)
