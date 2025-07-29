"""Defines the GroqPrompt node for configuring the OpenAi Prompt Driver.

This module provides the `GroqPrompt` class, which allows users
to configure and utilize the OpenAi prompt service within the Griptape
Nodes framework. It inherits common prompt parameters from `BasePrompt`, sets
Groq specific model options, requires a Groq API key via
node configuration, and instantiates the `OpenAiPromptDriver`.
"""

from griptape.drivers.prompt.openai import OpenAiChatPromptDriver as GtOpenAiChatPromptDriver

from griptape_nodes_library.config.prompt.base_prompt import BasePrompt

# --- Constants ---

SERVICE = "Groq"
BASE_URL = "https://api.groq.com/openai/v1"
API_KEY_URL = "https://console.groq.com/keys"
API_KEY_ENV_VAR = "GROQ_API_KEY"
MODEL_CHOICES = [
    "gemma2-9b-it",
    "meta-llama/llama-guard-4-12b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "allam-2-7b",
    "deepseek-r1-distill-llama-70b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
]
DEFAULT_MODEL = MODEL_CHOICES[0]


class GroqPrompt(BasePrompt):
    """Node for configuring and providing a Groq Chat Prompt Driver.

    Inherits from `BasePrompt` to leverage common LLM parameters. This node
    customizes the available models to those supported by Groq,
    removes parameters not applicable to Groq (like 'seed'), and
    requires a Groq API key to be set in the node's configuration
    under the 'Groq' service.

    The `process` method gathers the configured parameters and the API key,
    utilizes the `_get_common_driver_args` helper from `BasePrompt`, adds
    OpenAi specific configurations, then instantiates a
    `OpenAiPromptDriver` and assigns it to the 'prompt_model_config'
    output parameter.
    """

    def __init__(self, **kwargs) -> None:
        """Initializes the GroqPrompt node.

        Calls the superclass initializer, then modifies the inherited 'model'
        parameter to use Groq specific models and sets a default.
        It also removes the 'seed' parameter inherited from `BasePrompt` as it's
        not directly supported by the Groq driver implementation.
        """
        super().__init__(**kwargs)

        # --- Customize Inherited Parameters ---

        # Update the 'model' parameter for Groq specifics.
        self._update_option_choices(param="model", choices=MODEL_CHOICES, default=DEFAULT_MODEL)

        # Remove the 'seed' parameter as it's not directly used by GroqPromptDriver.
        self.remove_parameter_element_by_name("seed")

        # Remove `top_k` parameter as it's not used by Groq.
        self.remove_parameter_element_by_name("top_k")

        # Replace `min_p` with `top_p` for Groq.
        self._replace_param_by_name(param_name="min_p", new_param_name="top_p", default_value=0.9)

    def process(self) -> None:
        """Processes the node configuration to create a GroqPromptDriver.

        Retrieves parameter values set on the node and the required API key from
        the node's configuration system. It constructs the arguments dictionary
        for the `GroqPromptDriver`, handles optional parameters and
        any necessary conversions (like 'min_p' to 'top_p'), instantiates the
        driver, and assigns it to the 'prompt_model_config' output parameter.

        Raises:
            KeyError: If the Groq API key is not found in the node configuration
                      (though `validate_before_workflow_run` should prevent this during execution).
        """
        # Retrieve all parameter values set on the node UI or via input connections.
        params = self.parameter_values

        # --- Get Common Driver Arguments ---
        # Use the helper method from BasePrompt to get args like temperature, stream, max_attempts, etc.
        common_args = self._get_common_driver_args(params)

        # --- Prepare OpenAi Specific Arguments ---
        specific_args = {}

        # Retrieve the mandatory API key.
        specific_args["api_key"] = self.get_config_value(service=SERVICE, value=API_KEY_ENV_VAR)

        # Set the base URL for the Groq API.
        specific_args["base_url"] = BASE_URL

        # Get the selected model.
        specific_args["model"] = self.get_parameter_value("model")

        # Handle parameters that go into 'extra_params' for Groq.
        extra_params = {}

        extra_params["top_p"] = self.get_parameter_value("top_p")

        # Assign extra_params if not empty
        if extra_params:
            specific_args["extra_params"] = extra_params

        # --- Combine Arguments and Instantiate Driver ---
        # Combine common arguments with Groq specific arguments.
        # Specific args take precedence if there's an overlap (though unlikely here).
        all_kwargs = {**common_args, **specific_args}

        # Create the Groq prompt driver instance.
        driver = GtOpenAiChatPromptDriver(**all_kwargs)

        # Set the output parameter 'prompt_model_config'.
        self.parameter_output_values["prompt_model_config"] = driver

    def validate_before_workflow_run(self) -> list[Exception] | None:
        """Validates that the Groq API key is configured correctly.

        Calls the base class helper `_validate_api_key` with Groq-specific
        configuration details.
        """
        return self._validate_api_key(
            service_name=SERVICE,
            api_key_env_var=API_KEY_ENV_VAR,
            api_key_url=API_KEY_URL,
        )
