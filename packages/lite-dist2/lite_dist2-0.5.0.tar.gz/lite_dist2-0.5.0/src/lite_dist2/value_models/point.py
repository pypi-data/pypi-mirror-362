from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from lite_dist2.common import numerize, portablize
from lite_dist2.expections import LD2ModelTypeError
from lite_dist2.type_definitions import PortableValueType

if TYPE_CHECKING:
    from collections.abc import Iterable

    from lite_dist2.type_definitions import PrimitiveValueType, RawResultType


class BasePointValue(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def numerize(self) -> PrimitiveValueType | list[PrimitiveValueType]:
        pass

    @abc.abstractmethod
    def equal_to(self, other: BasePointValue) -> bool:
        pass

    @abc.abstractmethod
    def get_value_size(self) -> int:
        pass

    @abc.abstractmethod
    def get_value_types(self) -> tuple[Literal["bool", "int", "float"], ...]:
        pass

    @abc.abstractmethod
    def get_value_list(self) -> list[PortableValueType]:
        pass

    @abc.abstractmethod
    def to_dummy(self) -> BasePointValue:
        pass

    @staticmethod
    @abc.abstractmethod
    def create_from_numeric(
        raw_result_value: RawResultType,
        value_type: Literal["bool", "int", "float"],
        name: str | None = None,
    ) -> BasePointValue:
        pass

    @staticmethod
    def get_default_value(value_type: Literal["bool", "int", "float"]) -> PortableValueType:
        match value_type:
            case "bool":
                return False
            case "int":
                return "0x0"
            case "float":
                return "0x0.0p+0"
            case _:
                raise LD2ModelTypeError(value_type)


class ScalarValue(BaseModel, BasePointValue):
    type: Literal["scalar"]
    value_type: Literal["bool", "int", "float"]
    value: PortableValueType
    name: str | None = None

    def numerize(self) -> PrimitiveValueType:
        return numerize(self.value_type, self.value)

    def equal_to(self, other: BasePointValue) -> bool:
        if not isinstance(other, ScalarValue):
            return False
        return self.value_type == other.value_type and self.value == other.value

    def get_value_size(self) -> int:
        return 1

    def get_value_types(self) -> tuple[Literal["bool", "int", "float"], ...]:
        return (self.value_type,)

    def get_value_list(self) -> list[PortableValueType]:
        return [self.value]

    def to_dummy(self) -> ScalarValue:
        return ScalarValue(
            type="scalar",
            value_type=self.value_type,
            value=self.get_default_value(self.value_type),
            name=self.name,
        )

    @staticmethod
    def create_from_numeric(
        raw_result_value: RawResultType,
        value_type: Literal["bool", "int", "float"],
        name: str | None = None,
    ) -> ScalarValue:
        val = portablize(value_type, raw_result_value)
        return ScalarValue(type="scalar", value_type=value_type, value=val, name=name)


class VectorValue(BaseModel, BasePointValue):
    type: Literal["vector"]
    value_type: Literal["bool", "int", "float"]
    values: list[PortableValueType]
    name: str | None = None

    def numerize(self) -> list[PrimitiveValueType]:
        return [numerize(self.value_type, v) for v in self.values]

    def equal_to(self, other: BasePointValue) -> bool:
        if not isinstance(other, VectorValue):
            return False
        return self.value_type == other.value_type and self.values == other.values

    def get_value_size(self) -> int:
        return len(self.values)

    def get_value_types(self) -> tuple[Literal["bool", "int", "float"], ...]:
        return (self.value_type,) * self.get_value_size()

    def get_value_list(self) -> list[PortableValueType]:
        return self.values

    def to_dummy(self) -> BasePointValue:
        return VectorValue(
            type="vector",
            value_type=self.value_type,
            values=[self.get_default_value(self.value_type) for _ in self.values],
            name=self.name,
        )

    @staticmethod
    def create_from_numeric(
        raw_result_value: Iterable[RawResultType],
        value_type: Literal["bool", "int", "float"],
        name: str | None = None,
    ) -> VectorValue:
        val = [portablize(value_type, rv) for rv in raw_result_value]
        return VectorValue(type="vector", value_type=value_type, values=val, name=name)


type ParamType = tuple[ScalarValue, ...]
type ResultType = ScalarValue | VectorValue
