import logging
from abc import abstractmethod

import huggingface_hub

from diffusers_nodes_library.common.parameters.huggingface_repo_file_parameter import (
    HuggingFaceRepoFileParameter,  # type: ignore[reportMissingImports]
)
from diffusers_nodes_library.pipelines.wan.lora.wan_lora_parameters import (  # type: ignore[reportMissingImports]
    WanLoraParameters,  # type: ignore[reportMissingImports]
)
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import ControlNode

logger = logging.getLogger("diffusers_nodes_library")


class HuggingFaceWanLora(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        repo_file = self.get_repo_id(), self.get_filename()
        self.lora_revisions_params = HuggingFaceRepoFileParameter(
            self, repo_files=[repo_file], parameter_name="lora_model"
        )
        self.lora_weight_and_output_params = WanLoraParameters(self)

        self.add_parameters()

    def add_parameters(self) -> None:
        self.lora_revisions_params.add_input_parameters()
        self.lora_weight_and_output_params.add_input_parameters()
        trigger_phrase = self.get_trigger_phrase()
        if trigger_phrase is not None:
            self.add_parameter(
                Parameter(
                    name="trigger_phrase",
                    default_value=self.get_trigger_phrase(),
                    input_types=["str"],
                    type="str",
                    allowed_modes={ParameterMode.OUTPUT},
                    tooltip="a phrase that must be included in the prompt in order to trigger the lora",
                )
            )
        self.lora_weight_and_output_params.add_output_parameters()

    def process(self) -> None:
        repo_id, revision = self.lora_revisions_params.get_repo_revision()
        lora_path = huggingface_hub.hf_hub_download(
            repo_id=repo_id,
            revision=revision,
            filename=self.get_filename(),
            local_files_only=True,
        )
        lora_weight = self.lora_weight_and_output_params.get_weight()
        self.lora_weight_and_output_params.set_output_lora({lora_path: lora_weight})

    def validate_before_node_run(self) -> list[Exception] | None:
        errors = self.lora_revisions_params.validate_before_node_run()
        return errors or None

    @abstractmethod
    def get_repo_id(self) -> str: ...

    @abstractmethod
    def get_filename(self) -> str: ...

    @abstractmethod
    def get_trigger_phrase(self) -> str | None: ...
