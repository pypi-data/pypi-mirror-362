from typing import Literal

from pydantic import BaseModel

from lite_dist2.type_definitions import PortableValueType
from lite_dist2.value_models.aligned_space import ParameterAlignedSpaceModel
from lite_dist2.value_models.line_segment import LineSegmentModel


class LineSegmentRegistry(BaseModel):
    name: str | None = None
    type: Literal["bool", "int", "float"]
    size: str | None
    step: PortableValueType
    start: PortableValueType

    def to_line_segment_model(self) -> LineSegmentModel:
        return LineSegmentModel(
            name=self.name,
            type=self.type,
            size=self.size,
            step=self.step,
            start=self.start,
            ambient_index="0x0",
            ambient_size=self.size,
            is_dummy=False,
        )


class ParameterAlignedSpaceRegistry(BaseModel):
    type: Literal["aligned"]
    axes: list[LineSegmentRegistry]

    def to_parameter_aligned_space_model(self) -> ParameterAlignedSpaceModel:
        return ParameterAlignedSpaceModel(
            type=self.type,
            axes=[axis.to_line_segment_model() for axis in self.axes],
            check_lower_filling=True,
        )
