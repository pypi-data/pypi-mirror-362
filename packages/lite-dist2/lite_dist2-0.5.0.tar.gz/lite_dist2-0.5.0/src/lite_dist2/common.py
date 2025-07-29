from datetime import datetime, timedelta, timezone
from typing import Literal

from lite_dist2.expections import LD2ModelTypeError
from lite_dist2.type_definitions import PortableValueType, PrimitiveValueType


def hex2int(hex_str: str) -> int:
    return int(hex_str, base=16)


def int2hex(val: int) -> str:
    return hex(val)


def hex2float(hex_str: str) -> float:
    return float.fromhex(hex_str)


def float2hex(val: float) -> str:
    return val.hex()


def numerize(type_name: Literal["bool", "int", "float"], value: PortableValueType) -> PrimitiveValueType:
    match type_name:
        case "bool":
            return value
        case "int":
            return hex2int(value)
        case "float":
            return hex2float(value)
        case _:
            raise LD2ModelTypeError(type_name)


def portablize(type_name: Literal["bool", "int", "float"], value: PrimitiveValueType) -> PortableValueType:
    match type_name:
        case "bool":
            return value
        case "int":
            return int2hex(value)
        case "float":
            return float2hex(value)
        case _:
            raise LD2ModelTypeError(type_name)


def publish_timestamp() -> datetime:
    return datetime.now(tz=timezone(timedelta(hours=+9), "JST"))
