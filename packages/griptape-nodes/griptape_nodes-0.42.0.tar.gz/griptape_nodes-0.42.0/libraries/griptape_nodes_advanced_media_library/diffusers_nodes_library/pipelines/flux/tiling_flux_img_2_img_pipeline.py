import logging
from typing import Any

import diffusers  # type: ignore[reportMissingImports]
import PIL.Image
import torch  # type: ignore[reportMissingImports]
from griptape.artifacts import ImageUrlArtifact
from PIL.Image import Image
from pillow_nodes_library.utils import (  # type: ignore[reportMissingImports]
    image_artifact_to_pil,  # type: ignore[reportMissingImports]
    pil_to_image_artifact,  # type: ignore[reportMissingImports]
)
from utils.image_utils import load_image_from_url_artifact

from diffusers_nodes_library.common.misc.tiling_image_processor import (
    TilingImageProcessor,  # type: ignore[reportMissingImports]
)
from diffusers_nodes_library.common.parameters.log_parameter import (  # type: ignore[reportMissingImports]
    LogParameter,  # type: ignore[reportMissingImports]
)
from diffusers_nodes_library.common.utils.huggingface_utils import model_cache  # type: ignore[reportMissingImports]
from diffusers_nodes_library.common.utils.math_utils import next_multiple_ge  # type: ignore[reportMissingImports]
from diffusers_nodes_library.pipelines.flux.flux_loras_parameter import FluxLorasParameter
from diffusers_nodes_library.pipelines.flux.flux_pipeline_memory_footprint import (
    optimize_flux_pipeline_memory_footprint,
)  # type: ignore[reportMissingImports]
from diffusers_nodes_library.pipelines.flux.flux_pipeline_parameters import (
    FluxPipelineParameters,  # type: ignore[reportMissingImports]
)
from griptape_nodes.exe_types.core_types import Parameter
from griptape_nodes.exe_types.node_types import AsyncResult, ControlNode
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
from griptape_nodes.traits.options import Options

logger = logging.getLogger("diffusers_nodes_library")


class TilingFluxImg2ImgPipeline(ControlNode):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.flux_params = FluxPipelineParameters(self)
        self.add_parameter(
            Parameter(
                name="input_image",
                input_types=["ImageArtifact", "ImageUrlArtifact"],
                type="ImageArtifact",
                tooltip="input_image",
            )
        )
        self.flux_lora_params = FluxLorasParameter(self)
        self.log_params = LogParameter(self)
        self.flux_params.add_input_parameters()
        self.flux_lora_params.add_input_parameters()

        self.add_parameter(
            Parameter(
                name="strength",
                default_value=0.3,
                input_types=["float"],
                type="float",
                tooltip="strength (basically denoise) -- 0.0 is original image 1.0 is a completely new image -- impacts effective steps",
            )
        )
        self.add_parameter(
            Parameter(
                name="max_tile_size",
                default_value=1024,
                input_types=["int"],
                type="int",
                tooltip=(
                    "max_tile_size, "
                    "must be a multiple of 16, "
                    "if unecessily larger than input image, it will automatically "
                    "be lowered to smallest multiple of 16 that will fit the input image"
                ),
            )
        )
        self.add_parameter(
            Parameter(
                name="tile_overlap",
                default_value=64,
                input_types=["int"],
                type="int",
                tooltip="tile_overlap",
            )
        )
        self.add_parameter(
            Parameter(
                name="tile_strategy",
                default_value="linear",
                input_types=["str"],
                type="str",
                traits={
                    Options(
                        choices=[
                            "linear",
                            "chess",
                            "random",
                            "inward",
                            "outward",
                        ]
                    )
                },
                tooltip="tile_strategy",
            )
        )
        self.flux_params.add_output_parameters()
        self.log_params.add_output_parameters()

    def _get_temp_directory_path(self) -> str:
        """Get the configured temp directory path for this library."""
        # Get configured temp folder name, default to "intermediates"
        temp_folder_name = GriptapeNodes.ConfigManager().get_config_value("advanced_media_library.temp_folder_name")
        if temp_folder_name is None:
            temp_folder_name = "intermediates"
        return temp_folder_name

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        self.flux_params.after_value_set(parameter, value)

    def validate_before_node_run(self) -> list[Exception] | None:
        input_image = self.get_parameter_value("input_image")
        if input_image is None:
            return [ValueError("input_image is required")]
        return []

    def preprocess(self) -> None:
        self.flux_params.preprocess()

    def process(self) -> AsyncResult | None:
        yield lambda: self._process()

    def _process(self) -> AsyncResult | None:  # noqa: PLR0915
        self.preprocess()
        max_tile_size = int(self.get_parameter_value("max_tile_size"))
        input_image_artifact = self.get_parameter_value("input_image")
        tile_overlap = int(self.get_parameter_value("tile_overlap"))
        tile_strategy = str(self.get_parameter_value("tile_strategy"))
        strength = float(self.get_parameter_value("strength"))

        if isinstance(input_image_artifact, ImageUrlArtifact):
            input_image_artifact = load_image_from_url_artifact(input_image_artifact)
        input_image_pil = image_artifact_to_pil(input_image_artifact)
        input_image_pil = input_image_pil.convert("RGB")

        # The output image will be the same size as the input image.
        # Immediately set a preview placeholder image to make it react quickly and adjust
        # the size of the image preview on the node.
        preview_placeholder_image = PIL.Image.new("RGB", input_image_pil.size, color="black")
        self.publish_update_to_parameter(
            "output_image",
            pil_to_image_artifact(preview_placeholder_image, directory_path=self._get_temp_directory_path()),
        )

        # Adjust tile size so that it is not much bigger than the input image.
        largest_reasonable_tile_width = next_multiple_ge(input_image_pil.width, 16)
        largest_reasonable_tile_height = next_multiple_ge(input_image_pil.height, 16)
        largest_reasonable_tile_size = max(largest_reasonable_tile_height, largest_reasonable_tile_width)
        tile_size = min(largest_reasonable_tile_size, max_tile_size)

        if tile_size % 16 != 0:
            new_tile_size = next_multiple_ge(tile_size, 16)
            self.append_value_to_parameter(
                "logs", f"max_tile_size({tile_size}) not multiple of 16, rounding up to {new_tile_size}.\n"
            )
            tile_size = new_tile_size

        if strength == 0:
            self.set_parameter_value("output_image", pil_to_image_artifact(input_image_pil))
            return

        self.flux_params.publish_output_image_preview_placeholder()
        self.log_params.append_to_logs("Preparing models...\n")

        with self.log_params.append_profile_to_logs("Loading model metadata"):
            base_repo_id, base_revision = self.flux_params.get_repo_revision()
            pipe = model_cache.from_pretrained(
                diffusers.FluxImg2ImgPipeline,
                pretrained_model_name_or_path=base_repo_id,
                revision=base_revision,
                torch_dtype=torch.bfloat16,
                local_files_only=True,
            )

        with self.log_params.append_profile_to_logs("Loading model"), self.log_params.append_logs_to_logs(logger):
            optimize_flux_pipeline_memory_footprint(pipe)

        with (
            self.log_params.append_profile_to_logs("Configuring flux loras"),
            self.log_params.append_logs_to_logs(logger),
        ):
            self.flux_lora_params.configure_loras(pipe)

        num_inference_steps = self.flux_params.get_num_inference_steps()

        def wrapped_pipe(tile: Image, get_preview_image_with_partial_tile: Any) -> Image:
            def callback_on_step_end(
                pipe: diffusers.FluxImg2ImgPipeline, i: int, _t: Any, callback_kwargs: dict
            ) -> dict:
                if i < num_inference_steps - 1:
                    # Generate a preview image if this is not yet the last step.
                    # That would be redundant, since the pipeline automatically
                    # does that for the last step.
                    latents = callback_kwargs["latents"]
                    latents = pipe._unpack_latents(latents, tile_size, tile_size, pipe.vae_scale_factor)
                    latents = (latents / pipe.vae.config.scaling_factor) + pipe.vae.config.shift_factor
                    image = pipe.vae.decode(latents, return_dict=False)[0]
                    # TODO: https://github.com/griptape-ai/griptape-nodes/issues/845
                    intermediate_pil_image = pipe.image_processor.postprocess(image, output_type="pil")[0]

                    # HERE -> need to update the tile by calling something in the tile processor.
                    preview_image_with_partial_tile = get_preview_image_with_partial_tile(intermediate_pil_image)
                    self.publish_update_to_parameter(
                        "output_image",
                        pil_to_image_artifact(
                            preview_image_with_partial_tile, directory_path=self._get_temp_directory_path()
                        ),
                    )
                    self.append_value_to_parameter(
                        "logs", f"Finished inference step {i + 1} of {num_inference_steps}.\n"
                    )
                    self.append_value_to_parameter(
                        "logs", f"Starting inference step {i + 2} of {num_inference_steps}...\n"
                    )
                return {}

            flux_kwargs = self.flux_params.get_pipe_kwargs()
            flux_kwargs.pop("width")
            flux_kwargs.pop("height")
            return (
                pipe(
                    **flux_kwargs,
                    image=tile,
                    width=tile.width,
                    height=tile.height,
                    strength=strength,
                    output_type="pil",
                    callback_on_step_end=callback_on_step_end,
                )
                .images[0]
                .convert("RGB")
            )

        tiling_image_processor = TilingImageProcessor(
            pipe=wrapped_pipe,
            tile_size=tile_size,
            tile_overlap=tile_overlap,
            tile_strategy=tile_strategy,
        )
        num_tiles = tiling_image_processor.get_num_tiles(image=input_image_pil)

        def callback_on_tile_end(i: int, preview_image_pil: Image) -> None:
            if i < num_tiles:
                self.publish_update_to_parameter(
                    "output_image",
                    pil_to_image_artifact(preview_image_pil, directory_path=self._get_temp_directory_path()),
                )
                self.log_params.append_to_logs(f"Finished tile {i} of {num_tiles}.\n")
                self.log_params.append_to_logs(f"Starting tile {i + 1} of {num_tiles}...\n")

        self.log_params.append_to_logs(f"Starting tile 1 of {num_tiles}...\n")
        output_image_pil = tiling_image_processor.process(
            image=input_image_pil,
            callback_on_tile_end=callback_on_tile_end,
        )
        self.log_params.append_to_logs(f"Finished tile {num_tiles} of {num_tiles}.\n")
        self.set_parameter_value("output_image", pil_to_image_artifact(output_image_pil))
        self.parameter_output_values["output_image"] = pil_to_image_artifact(output_image_pil)
