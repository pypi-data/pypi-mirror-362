from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode, DataNode
from griptape_nodes.utils.dict_utils import to_dict


class ToDictionary(DataNode):
    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
        value: str = "",
    ) -> None:
        super().__init__(name, metadata)

        self.add_parameter(
            Parameter(
                name="from",
                default_value=value,
                input_types=["any"],
                tooltip="The data to convert",
                allowed_modes={ParameterMode.INPUT},
            )
        )
        self.add_parameter(
            Parameter(
                name="output",
                default_value=value,
                output_type="dict",
                type="dict",
                tooltip="The converted data as dict",
                ui_options={"hide_property": True},
                allowed_modes={ParameterMode.OUTPUT, ParameterMode.PROPERTY},
            )
        )

    def after_incoming_connection(
        self,
        source_node: BaseNode,
        source_parameter: Parameter,
        target_parameter: Parameter,
    ) -> None:
        pass

    def process(self) -> None:
        # Get the input value
        params = self.parameter_values

        input_value = params.get("from", {})

        self.parameter_output_values["output"] = to_dict(input_value)
