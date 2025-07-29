from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from lite_dist2.common import float2hex, int2hex, numerize
from lite_dist2.expections import LD2UndefinedError

if TYPE_CHECKING:
    from lite_dist2.type_definitions import ConstParamType


class ConstParamElement(BaseModel):
    type: Literal["int", "float", "bool", "str"]
    key: str
    value: bool | str

    def unpack(self) -> ConstParamType:
        match self.type:
            case "int" | "float" | "bool":
                return numerize(self.type, self.value)
            case "str":
                return self.value
            case _:
                raise LD2UndefinedError(self.type)

    @staticmethod
    def from_kv(key: str, value: ConstParamType) -> ConstParamElement:
        match value:
            case bool():
                return ConstParamElement(type="bool", key=key, value=value)
            case int():
                return ConstParamElement(type="int", key=key, value=int2hex(value))
            case float():
                return ConstParamElement(type="float", key=key, value=float2hex(value))
            case str():
                return ConstParamElement(type="str", key=key, value=value)
            case _:
                raise LD2UndefinedError(type(value))


class ConstParam(BaseModel):
    consts: list[ConstParamElement]

    def to_dict(self) -> dict[str, ConstParamType]:
        return {const.key: const.unpack() for const in self.consts}

    @staticmethod
    def from_dict(d: dict[str, ConstParamType]) -> ConstParam:
        return ConstParam(consts=[ConstParamElement.from_kv(k, v) for k, v in d.items()])
