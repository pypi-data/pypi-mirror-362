from typing import Any

from griptape_nodes.exe_types.core_types import (
    Parameter,
)
from griptape_nodes.exe_types.node_types import DataNode


class DisplayInteger(DataNode):
    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
        value: int = 0,
    ) -> None:
        super().__init__(name, metadata)

        self.value = value
        self.add_parameter(
            Parameter(
                name="integer",
                default_value=self.value,
                type="int",
                tooltip="The number to display",
            )
        )

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        if "integer" in parameter.name:
            self.parameter_output_values["integer"] = value
            self.publish_update_to_parameter("integer", value)
        return super().after_value_set(parameter, value)

    def process(self) -> None:
        self.parameter_output_values["integer"] = self.parameter_values.get("integer")
