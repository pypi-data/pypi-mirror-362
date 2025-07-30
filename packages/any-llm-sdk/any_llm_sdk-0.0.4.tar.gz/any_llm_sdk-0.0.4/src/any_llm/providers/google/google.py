import os
import json
from typing import Any

try:
    from google import genai
    from google.genai import types
except ImportError:
    msg = "google-genai is not installed. Please install it with `pip install any-llm-sdk[google]`"
    raise ImportError(msg)

from pydantic import BaseModel

from openai._streaming import Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion import ChatCompletion
from any_llm.provider import Provider, ApiConfig
from any_llm.exceptions import MissingApiKeyError, UnsupportedParameterError
from any_llm.providers.base_framework import (
    create_completion_from_response,
)


def _convert_tool_spec(openai_tools: list[dict[str, Any]]) -> list[types.Tool]:
    """Convert OpenAI tool specification to Google GenAI format."""
    function_declarations = []

    for tool in openai_tools:
        if tool.get("type") != "function":
            continue

        function = tool["function"]
        parameters_dict = {
            "type": "object",
            "properties": {
                param_name: {
                    "type": param_info.get("type", "string"),
                    "description": param_info.get("description", ""),
                    **({"enum": param_info["enum"]} if "enum" in param_info else {}),
                }
                for param_name, param_info in function["parameters"]["properties"].items()
            },
            "required": function["parameters"].get("required", []),
        }

        function_declarations.append(
            types.FunctionDeclaration(
                name=function["name"],
                description=function.get("description", ""),
                parameters=types.Schema(**parameters_dict),
            )
        )

    return [types.Tool(function_declarations=function_declarations)]


def _convert_messages(messages: list[dict[str, Any]]) -> list[types.Content]:
    """Convert messages to Google GenAI format."""
    formatted_messages = []

    for message in messages:
        if message["role"] == "system":
            # System messages are treated as user messages in GenAI
            parts = [types.Part.from_text(text=message["content"])]
            formatted_messages.append(types.Content(role="user", parts=parts))
        elif message["role"] == "user":
            parts = [types.Part.from_text(text=message["content"])]
            formatted_messages.append(types.Content(role="user", parts=parts))
        elif message["role"] == "assistant":
            if "tool_calls" in message and message["tool_calls"]:
                # Handle function calls
                tool_call = message["tool_calls"][0]  # Assuming single function call for now
                function_call = tool_call["function"]

                parts = [
                    types.Part.from_function_call(
                        name=function_call["name"], args=json.loads(function_call["arguments"])
                    )
                ]
            else:
                # Handle regular text messages
                parts = [types.Part.from_text(text=message["content"])]

            formatted_messages.append(types.Content(role="model", parts=parts))
        elif message["role"] == "tool":
            # Convert tool result to function response
            try:
                content_json = json.loads(message["content"])
                part = types.Part.from_function_response(name=message.get("name", "unknown"), response=content_json)
                formatted_messages.append(types.Content(role="function", parts=[part]))
            except json.JSONDecodeError:
                # If not JSON, treat as text
                part = types.Part.from_function_response(
                    name=message.get("name", "unknown"), response={"result": message["content"]}
                )
                formatted_messages.append(types.Content(role="function", parts=[part]))

    return formatted_messages


class GoogleProvider(Provider):
    """Google Provider using the new response conversion utilities."""

    PROVIDER_NAME = "Google"

    def __init__(self, config: ApiConfig) -> None:
        """Initialize Google GenAI provider."""
        # Check if we should use Vertex AI or Gemini Developer API
        self.use_vertex_ai = os.getenv("GOOGLE_USE_VERTEX_AI", "false").lower() == "true"

        if self.use_vertex_ai:
            # Vertex AI configuration
            self.project_id = os.getenv("GOOGLE_PROJECT_ID")
            self.location = os.getenv("GOOGLE_REGION", "us-central1")

            if not self.project_id:
                raise MissingApiKeyError("Google Vertex AI", "GOOGLE_PROJECT_ID")

            # Initialize client for Vertex AI
            self.client = genai.Client(vertexai=True, project=self.project_id, location=self.location)
        else:
            # Gemini Developer API configuration
            # Use api_key from config if provided, otherwise fall back to environment variables
            api_key = getattr(config, "api_key", None) or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise MissingApiKeyError("Google Gemini Developer API", "GEMINI_API_KEY/GOOGLE_API_KEY")

            # Initialize client for Gemini Developer API
            self.client = genai.Client(api_key=api_key)

    def completion(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """Create a chat completion using Google GenAI."""

        if kwargs.get("stream", False) is True:
            raise UnsupportedParameterError("stream", "Google")

        # Handle response_format for Pydantic models
        response_schema = None
        if "response_format" in kwargs:
            response_format = kwargs.pop("response_format")
            if isinstance(response_format, type) and issubclass(response_format, BaseModel):
                # Use native Google GenAI schema configuration
                response_schema = response_format
                # Set the response mime type for JSON output
                kwargs["response_mime_type"] = "application/json"

        # Remove other unsupported parameters
        if "parallel_tool_calls" in kwargs:
            raise UnsupportedParameterError("parallel_tool_calls", self.PROVIDER_NAME)

        # Convert tools if present
        tools = None
        if "tools" in kwargs:
            tools = _convert_tool_spec(kwargs["tools"])
            kwargs["tools"] = tools

        # Convert messages to GenAI format
        formatted_messages = _convert_messages(messages)

        # Create generation config
        generation_config = types.GenerateContentConfig(
            **kwargs,
        )

        # For now, let's use a simple string-based approach
        content_text = ""
        if len(formatted_messages) == 1 and formatted_messages[0].role == "user":
            # Single user message
            parts = formatted_messages[0].parts
            if parts and hasattr(parts[0], "text"):
                content_text = parts[0].text or ""
            else:
                content_text = "Hello"  # fallback
        else:
            # Multiple messages - concatenate user messages for simplicity
            content_parts = []
            for msg in formatted_messages:
                if msg.role == "user" and msg.parts:
                    if hasattr(msg.parts[0], "text") and msg.parts[0].text:
                        content_parts.append(msg.parts[0].text)

            content_text = "\n".join(content_parts)
            if not content_text:
                content_text = "Hello"  # fallback

        # Generate content using the client with schema if provided
        if response_schema:
            # Add response_schema to the config
            generation_config.response_schema = response_schema
            response = self.client.models.generate_content(model=model, contents=content_text, config=generation_config)
        else:
            response = self.client.models.generate_content(model=model, contents=content_text, config=generation_config)

        # Convert response to dict-like structure for the utility
        response_dict = {
            "id": "google_genai_response",
            "model": "google/genai",
            "created": 0,
            "usage": {
                "prompt_tokens": getattr(response.usage_metadata, "prompt_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0,
                "completion_tokens": getattr(response.usage_metadata, "candidates_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0,
                "total_tokens": getattr(response.usage_metadata, "total_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0,
            },
        }

        # Check if the response contains function calls
        if (
            response.candidates
            and len(response.candidates) > 0
            and response.candidates[0].content
            and response.candidates[0].content.parts
            and len(response.candidates[0].content.parts) > 0
            and hasattr(response.candidates[0].content.parts[0], "function_call")
            and response.candidates[0].content.parts[0].function_call
        ):
            function_call = response.candidates[0].content.parts[0].function_call

            # Convert the function call arguments to a dictionary
            args_dict = {}
            if hasattr(function_call, "args") and function_call.args:
                for key, value in function_call.args.items():
                    args_dict[key] = value

            response_dict["choices"] = [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": f"call_{hash(function_call.name)}",
                                "function": {
                                    "name": function_call.name,
                                    "arguments": json.dumps(args_dict),
                                },
                                "type": "function",
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                    "index": 0,
                }
            ]
        else:
            # Handle regular text response
            content = ""
            if (
                response.candidates
                and len(response.candidates) > 0
                and response.candidates[0].content
                and response.candidates[0].content.parts
                and len(response.candidates[0].content.parts) > 0
                and hasattr(response.candidates[0].content.parts[0], "text")
            ):
                content = response.candidates[0].content.parts[0].text or ""

            response_dict["choices"] = [
                {
                    "message": {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": None,
                    },
                    "finish_reason": "stop",
                    "index": 0,
                }
            ]

        # Convert to OpenAI format using the new utility
        return create_completion_from_response(
            response_data=response_dict,
            model=model,
            provider_name="google",
        )
