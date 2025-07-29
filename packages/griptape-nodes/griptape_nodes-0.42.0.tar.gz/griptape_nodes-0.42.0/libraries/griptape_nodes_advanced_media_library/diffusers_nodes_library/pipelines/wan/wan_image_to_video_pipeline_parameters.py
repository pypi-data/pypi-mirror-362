import logging
import tempfile
import uuid
from pathlib import Path
from typing import Any

import diffusers  # type: ignore[reportMissingImports]
import numpy as np
import PIL.Image
import torch  # type: ignore[reportMissingImports]
from artifact_utils.video_url_artifact import VideoUrlArtifact  # type: ignore[reportMissingImports]
from griptape.artifacts import ImageUrlArtifact
from griptape.loaders import ImageLoader
from PIL.Image import Image
from pillow_nodes_library.utils import (  # type: ignore[reportMissingImports]
    image_artifact_to_pil,
)

from diffusers_nodes_library.common.parameters.huggingface_repo_parameter import HuggingFaceRepoParameter
from diffusers_nodes_library.common.parameters.seed_parameter import SeedParameter
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import BaseNode
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

logger = logging.getLogger("diffusers_nodes_library")


class WanImageToVideoPipelineParameters:
    def __init__(self, node: BaseNode):
        self._node = node
        self._huggingface_repo_parameter = HuggingFaceRepoParameter(
            node,
            repo_ids=[
                "Wan-AI/Wan2.1-I2V-14B-480P-Diffusers",
                "Wan-AI/Wan2.1-I2V-14B-720P-Diffusers",
            ],
        )
        self._seed_parameter = SeedParameter(node)

    def add_input_parameters(self) -> None:
        self._huggingface_repo_parameter.add_input_parameters()

        default_width, default_height = self._get_model_defaults()

        self._node.add_parameter(
            Parameter(
                name="input_image",
                input_types=["ImageArtifact", "ImageUrlArtifact"],
                type="ImageArtifact",
                tooltip="Input image for video generation",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="auto_resize_input_image",
                default_value=True,
                input_types=["bool"],
                type="bool",
                tooltip="Automatically resize input image to match model requirements",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="prompt",
                default_value="",
                input_types=["str"],
                type="str",
                tooltip="Prompt for video generation",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="negative_prompt",
                default_value="",
                input_types=["str"],
                type="str",
                tooltip="Negative prompt (optional)",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="width",
                default_value=default_width,
                input_types=["int"],
                type="int",
                allowed_modes=set(),
                tooltip="Video frame width (model-specific)",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="height",
                default_value=default_height,
                input_types=["int"],
                type="int",
                allowed_modes=set(),
                tooltip="Video frame height (model-specific)",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="num_frames",
                default_value=33,
                input_types=["int"],
                type="int",
                tooltip="Number of frames to generate (model-specific)",
                ui_options={"slider": {"min_val": 9, "max_val": 65}, "step": 8},
            )
        )
        self._node.add_parameter(
            Parameter(
                name="num_inference_steps",
                default_value=50,
                input_types=["int"],
                type="int",
                tooltip="Number of denoising steps (20 is quick, 50+ for quality)",
            )
        )
        self._node.add_parameter(
            Parameter(
                name="guidance_scale",
                default_value=5.0,
                input_types=["float"],
                type="float",
                tooltip="CFG guidance scale (higher = more prompt adherence)",
            )
        )
        self._seed_parameter.add_input_parameters()

    def add_output_parameters(self) -> None:
        self._node.add_parameter(
            Parameter(
                name="output_video",
                output_type="VideoUrlArtifact",
                tooltip="The output video",
                allowed_modes={ParameterMode.OUTPUT},
            )
        )

    def validate_before_node_run(self) -> list[Exception] | None:
        errors = self._huggingface_repo_parameter.validate_before_node_run()

        # Validate dimensions are divisible by 16
        width = self.get_width()
        height = self.get_height()
        if width % 16 != 0:
            errors = errors or []
            errors.append(ValueError(f"Width ({width}) must be divisible by 16"))
        if height % 16 != 0:
            errors = errors or []
            errors.append(ValueError(f"Height ({height}) must be divisible by 16"))

        return errors or None

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        self._seed_parameter.after_value_set(parameter, value)
        self._update_dimensions_for_model(parameter, value)

    def preprocess(self) -> None:
        self._seed_parameter.preprocess()

    def get_repo_revision(self) -> tuple[str, str]:
        return self._huggingface_repo_parameter.get_repo_revision()

    def publish_output_video_preview_placeholder(self) -> None:
        # Create a small black video placeholder
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        try:
            # Create a single black frame and export as 1-frame video

            black_frame = PIL.Image.new("RGB", (320, 240), color="black")
            frames = [black_frame]
            diffusers.utils.export_to_video(frames, str(temp_path), fps=1)
            filename = f"placeholder_{uuid.uuid4()}.mp4"
            url = GriptapeNodes.StaticFilesManager().save_static_file(temp_path.read_bytes(), filename)
            self._node.publish_update_to_parameter("output_video", VideoUrlArtifact(url))
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def get_input_image_pil(self) -> Image:
        input_image_artifact = self._node.get_parameter_value("input_image")
        if isinstance(input_image_artifact, ImageUrlArtifact):
            input_image_artifact = ImageLoader().parse(input_image_artifact.to_bytes())
        input_image_pil = image_artifact_to_pil(input_image_artifact)
        return input_image_pil.convert("RGB")

    def get_auto_resize_input_image(self) -> bool:
        return bool(self._node.get_parameter_value("auto_resize_input_image"))

    def get_prompt(self) -> str:
        return self._node.get_parameter_value("prompt")

    def get_negative_prompt(self) -> str:
        return self._node.get_parameter_value("negative_prompt")

    def get_width(self) -> int:
        return int(self._node.get_parameter_value("width"))

    def get_height(self) -> int:
        return int(self._node.get_parameter_value("height"))

    def get_num_frames(self) -> int:
        return int(self._node.get_parameter_value("num_frames"))

    def get_num_inference_steps(self) -> int:
        return int(self._node.get_parameter_value("num_inference_steps"))

    def get_guidance_scale(self) -> float:
        return float(self._node.get_parameter_value("guidance_scale"))

    def _get_model_defaults(self, repo_id: str | None = None) -> tuple[int, int]:
        """Get default width and height for a specific model or the default model."""
        if repo_id is None:
            available_models = self._huggingface_repo_parameter.fetch_repo_revisions()
            if not available_models:
                return 832, 480  # Default to 832x480 if no models are available
            repo_id = available_models[0][0]

        match repo_id:
            case "Wan-AI/Wan2.1-I2V-14B-480P-Diffusers":
                return 832, 480  # I2V 480P model - optimized for consumer GPUs
            case "Wan-AI/Wan2.1-I2V-14B-720P-Diffusers":
                return 1280, 720  # I2V 720P model - higher resolution
            case _:
                msg = f"Unsupported model repo_id: {repo_id}."
                raise ValueError(msg)

    def _update_dimensions_for_model(self, parameter: Parameter, value: Any) -> None:
        """Update width and height when model selection changes."""
        if parameter.name == "model" and isinstance(value, str):
            repo_id, _ = self._huggingface_repo_parameter._key_to_repo_revision(value)
            recommended_width, recommended_height = self._get_model_defaults(repo_id)

            # Update dimensions
            current_width = self._node.get_parameter_value("width")
            current_height = self._node.get_parameter_value("height")

            if current_width != recommended_width:
                self._node.set_parameter_value("width", recommended_width)

            if current_height != recommended_height:
                self._node.set_parameter_value("height", recommended_height)

    def get_image_for_model(self, pipe: Any) -> tuple[Image, int, int]:
        """Prepare input image with proper resizing and update pipe_kwargs."""
        image = self.get_input_image_pil()
        repo_id, _ = self.get_repo_revision()

        if not self.get_auto_resize_input_image():
            # If auto-resize is disabled, ensure image matches model dimensions
            width = self.get_width()
            height = self.get_height()
            if image.width != width or image.height != height:
                msg = f"Input image must be {width}x{height} for model {repo_id}, but got {image.width}x{image.height}."
                raise ValueError(msg)
            return image, height, width

        # Automatically resize image based on model capabilities
        match repo_id:
            case "Wan-AI/Wan2.1-I2V-14B-480P-Diffusers":
                max_area = 832 * 480  # I2V 480P model
            case "Wan-AI/Wan2.1-I2V-14B-720P-Diffusers":
                max_area = 1280 * 720  # I2V 720P model
            case _:
                msg = f"Unsupported model repo_id: {repo_id}."
                raise ValueError(msg)

        aspect_ratio = image.height / image.width
        mod_value = pipe.vae_scale_factor_spatial * pipe.transformer.config.patch_size[1]
        height = round(np.sqrt(max_area * aspect_ratio)) // mod_value * mod_value
        width = round(np.sqrt(max_area / aspect_ratio)) // mod_value * mod_value
        image = image.resize((width, height))

        return image, height, width

    def get_pipe_kwargs(self, pipe: Any) -> dict:
        image, height, width = self.get_image_for_model(pipe)
        return {
            "prompt": self.get_prompt(),
            "negative_prompt": self.get_negative_prompt(),
            "image": image,
            "height": height,
            "width": width,
            "num_frames": self.get_num_frames(),
            "num_inference_steps": self.get_num_inference_steps(),
            "guidance_scale": self.get_guidance_scale(),
            "generator": self._seed_parameter.get_generator(),
        }

    def latents_to_video_mp4(self, pipe: Any, latents: Any) -> Path:
        """Convert latents to video frames and export as MP4 file."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file_obj:
            temp_file = Path(temp_file_obj.name)

        try:
            # Convert latents to video frames using VAE decode
            latents = latents.to(pipe.vae.dtype)

            # Apply latents normalization as per the WAN pipeline
            latents_mean = (
                torch.tensor(pipe.vae.config.latents_mean)
                .view(1, pipe.vae.config.z_dim, 1, 1, 1)
                .to(latents.device, latents.dtype)
            )
            latents_std = 1.0 / torch.tensor(pipe.vae.config.latents_std).view(1, pipe.vae.config.z_dim, 1, 1, 1).to(
                latents.device, latents.dtype
            )
            latents = latents / latents_std + latents_mean

            # Decode latents to video using VAE
            video = pipe.vae.decode(latents, return_dict=False)[0]
            frames = pipe.video_processor.postprocess_video(video, output_type="pil")[0]

            # Export frames to video
            diffusers.utils.export_to_video(frames, str(temp_file), fps=16)
        except Exception:
            # Clean up on error
            if temp_file.exists():
                temp_file.unlink()
            raise
        else:
            return temp_file

    def publish_output_video_preview_latents(self, pipe: Any, latents: Any) -> None:
        """Publish a preview video from latents during generation."""
        preview_video_path = None
        try:
            preview_video_path = self.latents_to_video_mp4(pipe, latents)
            filename = f"preview_{uuid.uuid4()}.mp4"
            url = GriptapeNodes.StaticFilesManager().save_static_file(preview_video_path.read_bytes(), filename)
            self._node.publish_update_to_parameter("output_video", VideoUrlArtifact(url))
        except Exception as e:
            logger.warning("Failed to generate video preview from latents: %s", e)
        finally:
            # Clean up temporary file
            if preview_video_path is not None and preview_video_path.exists():
                preview_video_path.unlink()

    def publish_output_video(self, video_path: Path) -> None:
        filename = f"{uuid.uuid4()}{video_path.suffix}"
        url = GriptapeNodes.StaticFilesManager().save_static_file(video_path.read_bytes(), filename)
        self._node.parameter_output_values["output_video"] = VideoUrlArtifact(url)
