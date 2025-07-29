import pytest

from lite_dist2.expections import LD2UndefinedError
from lite_dist2.value_models.const_param import ConstParam, ConstParamElement


def test_const_param_to_dict_from_dict() -> None:
    original = ConstParam(
        consts=[
            ConstParamElement(type="int", key="int_value", value="0x2"),
            ConstParamElement(type="float", key="float_value", value="0x1.0000000000000p+0"),
            ConstParamElement(type="bool", key="bool_value", value=False),
            ConstParamElement(type="str", key="str_value", value="rk"),
        ],
    )

    d = original.to_dict()
    actual = ConstParam.from_dict(d)
    assert original == actual


def test_const_param_element_from_kv_raise_undefined_type() -> None:
    with pytest.raises(LD2UndefinedError):
        # noinspection PyTypeChecker
        _ = ConstParamElement.from_kv(key="error_value", value=[])
