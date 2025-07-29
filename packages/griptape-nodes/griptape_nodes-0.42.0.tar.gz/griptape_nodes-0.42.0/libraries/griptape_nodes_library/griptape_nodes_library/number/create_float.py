from typing import Any

from griptape_nodes.exe_types.core_types import (
    Parameter,
    ParameterMode,
)
from griptape_nodes.exe_types.node_types import DataNode


class FloatInput(DataNode):
    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
        value: float = 0.0,
    ) -> None:
        super().__init__(name, metadata)

        self.value = value
        self.add_parameter(
            Parameter(
                name="float",
                default_value=self.value,
                output_type="float",
                type="float",
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
                tooltip="A float value",
            )
        )

    def process(self) -> None:
        self.parameter_output_values["float"] = self.parameter_values.get("float")
