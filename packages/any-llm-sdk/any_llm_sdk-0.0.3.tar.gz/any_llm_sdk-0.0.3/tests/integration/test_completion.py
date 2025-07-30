import httpx
from pydantic import BaseModel
import pytest
from any_llm import completion, ProviderName
from any_llm.exceptions import MissingApiKeyError


# Use small models for testing to make sure they work
provider_model_map = {
    ProviderName.MISTRAL: "mistral-small-latest",
    ProviderName.ANTHROPIC: "claude-3-5-sonnet-20240620",
    ProviderName.DEEPSEEK: "deepseek-chat",
    ProviderName.OPENAI: "gpt-4.1-mini",
    ProviderName.GOOGLE: "gemini-2.0-flash-001",
    ProviderName.MOONSHOT: "moonshot-v1-8k",
    ProviderName.SAMBANOVA: "sambanova-7b-instruct",
    ProviderName.TOGETHER: "meta-llama/Meta-Llama-3-8B-Instruct",
    ProviderName.XAI: "xai-3-70b-instruct",
    ProviderName.INCEPTION: "inception-3-70b-instruct",
    ProviderName.NEBIUS: "nebius-3-70b-instruct",
    ProviderName.OLLAMA: "llama3.2:3b",
    ProviderName.AZURE: "gpt-4o",
    ProviderName.COHERE: "command-r-20240215",
    ProviderName.CEREBRAS: "llama3.1-8b",
    ProviderName.HUGGINGFACE: "meta-llama/Meta-Llama-3-8B-Instruct",  # You must have novita enabled in your hf account to use this model
    ProviderName.AWS: "amazon.titan-text-001",
    ProviderName.WATSONX: "google/gemini-2.0-flash-001",
    ProviderName.FIREWORKS: "meta-llama/Meta-Llama-3-8B-Instruct",
    ProviderName.GROQ: "llama-3.1-8b-instant",
}


def test_providers(provider: ProviderName) -> None:
    """Test that all supported providers can be loaded successfully."""
    model_id = provider_model_map[provider]
    try:
        result = completion(f"{provider.value}/{model_id}", messages=[{"role": "user", "content": "Hello"}])
    except MissingApiKeyError:
        pytest.skip(f"{provider.value} API key not provided, skipping")
    except (httpx.HTTPStatusError, httpx.ConnectError):
        if provider == ProviderName.OLLAMA:
            pytest.skip("Ollama is not set up, skipping")
        raise
    assert result.choices[0].message.content is not None


def test_response_format(provider: ProviderName) -> None:
    """Test that all supported providers can be loaded successfully."""
    if provider == ProviderName.ANTHROPIC:
        pytest.skip("Anthropic does not support response_format")
        return
    model_id = provider_model_map[provider]

    class ResponseFormat(BaseModel):
        name: str

    prompt = "What is the capital of France?"
    try:
        result = completion(
            f"{provider.value}/{model_id}",
            messages=[{"role": "user", "content": prompt}],
            response_format=ResponseFormat,
        )
        assert result.choices[0].message.content is not None
        output = ResponseFormat.model_validate_json(result.choices[0].message.content)
        assert output.name == "Paris"
    except MissingApiKeyError:
        pytest.skip(f"{provider.value} API key not provided, skipping")
    except (httpx.HTTPStatusError, httpx.ConnectError):
        if provider == ProviderName.OLLAMA:
            pytest.skip("Ollama is not set up, skipping")
        raise
