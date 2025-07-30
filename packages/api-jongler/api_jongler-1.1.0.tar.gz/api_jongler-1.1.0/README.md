# API Jongler

A middleware utility for calling Google AI APIs (Gemini and Gemma) using multiple API keys to reduce the need for paid tiers.

## Description

APIJongler is a Python utility that manages multiple API keys for Google AI services (Gemini) and Hugging Face Gemma models, automatically handles key rotation, and provides optional Tor connectivity for enhanced privacy. It's designed to help developers distribute API calls across multiple keys to stay within free tier limits and seamlessly work with both Google's Gemini API and open-source Gemma models.

## Features

- **Google AI Integration**: Seamless access to both Gemini API and Gemma models via Hugging Face
- **Multiple API Key Management**: Automatically rotates between available API keys to maximize free tier usage
- **Lock Management**: Prevents concurrent use of the same API key across multiple processes
- **Error Handling**: Tracks and avoids problematic API keys automatically
- **Tor Support**: Optional routing through Tor network for enhanced privacy
- **Extensible**: Easy to add new API connectors via JSON configuration
- **Comprehensive Logging**: Configurable logging with colored console output

## Installation

```bash
pip install api-jongler
```

## Configuration

1. Set the configuration file path:
```bash
export APIJONGLER_CONFIG=/path/to/your/APIJongler.ini
```

2. Create your configuration file (APIJongler.ini):
```ini
[generativelanguage.googleapis.com]
key1 = your-gemini-api-key-1
key2 = your-gemini-api-key-2
key3 = your-gemini-api-key-3

[api-inference.huggingface.co]
key1 = hf_your-huggingface-token-1
key2 = hf_your-huggingface-token-2
key3 = hf_your-huggingface-token-3
```

**Note**: 
- For Google Gemini API keys, get them free at [Google AI Studio](https://aistudio.google.com/app/apikey).
- For Gemma models via Hugging Face, get API tokens at [Hugging Face Settings](https://huggingface.co/settings/tokens).

## Usage

### Basic Example with Google Gemini (Free Tier)

```python
from api_jongler import APIJongler

# Initialize with Gemini connector
jongler = APIJongler("generativelanguage.googleapis.com", is_tor_enabled=False)

# Use Gemini 1.5 Flash (free tier) for text generation
response, status_code = jongler.request(
    method="POST",
    endpoint="/v1beta/models/gemini-1.5-flash:generateContent",
    request='{"contents":[{"parts":[{"text":"Hello, how are you?"}]}]}'
)

print(f"Response: {response}")
print(f"Status Code: {status_code}")

# Clean up when done (automatically called on destruction)
del jongler

# Or manually clean up all locks and errors
APIJongler.cleanUp()
```

### Working with JSON Data (Recommended)

```python
from api_jongler import APIJongler

# Initialize with Gemini connector
jongler = APIJongler("generativelanguage.googleapis.com")

# Use requestJSON() for automatic JSON handling (recommended)
response_data = jongler.requestJSON(
    endpoint="/v1beta/models/gemini-1.5-flash:generateContent",
    data={
        "contents": [{"parts": [{"text": "Explain machine learning"}]}]
    }
)

# Response is automatically parsed as dictionary
print(response_data["candidates"][0]["content"]["parts"][0]["text"])
```

### Method Comparison

APIJongler provides two methods for making requests:

| Method | Input | Output | Use Case |
|--------|--------|---------|----------|
| `request()` | Raw string | `(response_text, status_code)` | Low-level control, non-JSON APIs |
| `requestJSON()` | Python dict | Parsed dictionary | JSON APIs (recommended) |

**Example with both methods:**

```python
# Low-level with request()
response_text, status_code = jongler.request(
    method="POST",
    endpoint="/v1beta/models/gemini-1.5-flash:generateContent", 
    request='{"contents":[{"parts":[{"text":"Hello"}]}]}'  # Raw JSON string
)
import json
data = json.loads(response_text)  # Manual parsing

# High-level with requestJSON() 
data = jongler.requestJSON(
    endpoint="/v1beta/models/gemini-1.5-flash:generateContent",
    data={"contents": [{"parts": [{"text": "Hello"}]}]}  # Python dict
)
# No manual parsing needed
```

### Available Gemini Models

The Gemini connector provides access to these models:

| Model | Description | Free Tier | Best For |
|-------|-------------|-----------|----------|
| `gemini-1.5-flash` | Fast and versatile | ✅ Yes | General tasks, quick responses |
| `gemini-2.0-flash` | Latest generation | ✅ Yes | Modern features, enhanced speed |
| `gemini-2.5-flash` | Best price/performance | Paid | Cost-effective quality responses |
| `gemini-2.5-pro` | Most powerful | Paid | Complex reasoning, advanced tasks |
| `gemini-1.5-pro` | Complex reasoning | Paid | Advanced analysis, coding |

### CLI Usage Examples

```bash
# Quick text generation (free tier)
apijongler generativelanguage.googleapis.com POST /v1beta/models/gemini-1.5-flash:generateContent '{"contents":[{"parts":[{"text":"Hello"}]}]}' --pretty

# Code generation (free tier)  
apijongler generativelanguage.googleapis.com POST /v1beta/models/gemini-2.0-flash:generateContent '{"contents":[{"parts":[{"text":"Write a Python function"}]}]}' --pretty

# Advanced reasoning (requires paid tier)
apijongler generativelanguage.googleapis.com POST /v1beta/models/gemini-2.5-pro:generateContent '{"contents":[{"parts":[{"text":"Analyze this problem"}]}]}' --pretty
```

## API Connectors

API connectors are defined in JSON files in the `connectors/` directory. Example:

```json
{
    "name": "generativelanguage.googleapis.com",
    "host": "generativelanguage.googleapis.com",
    "port": 443,
    "protocol": "https",
    "format": "json",
    "requires_api_key": true
}
```

### Pre-configured Connectors

- **generativelanguage.googleapis.com**: Access to Google's Gemini API models (gemini-1.5-flash, gemini-2.0-flash, gemini-2.5-flash, etc.)
- **api-inference.huggingface.co**: Open-source Gemma models via Hugging Face Inference API (gemma-2-9b-it, gemma-2-27b-it, etc.)
- **httpbin.org**: For testing and development purposes only

### Gemma vs Gemini Models

**Important**: Gemma and Gemini are different model families:

| Model Family | Access Method | API Keys Source | Example Model |
|--------------|---------------|-----------------|---------------|
| **Gemini** | Google's Cloud API | [Google AI Studio](https://aistudio.google.com/app/apikey) | gemini-1.5-flash |
| **Gemma** | Hugging Face Inference API | [HuggingFace Tokens](https://huggingface.co/settings/tokens) | google/gemma-2-9b-it |

#### Gemma Usage Examples

```python
from api_jongler import APIJongler

# Use Gemma 2 9B model
jongler = APIJongler("api-inference.huggingface.co")
response = jongler.requestJSON(
    endpoint="/models/google/gemma-2-9b-it",
    data={
        "inputs": "What is machine learning?",
        "parameters": {"max_new_tokens": 100, "temperature": 0.7}
    }
)
print(response)
```

```bash
# CLI usage for Gemma
apijongler api-inference.huggingface.co POST /models/google/gemma-2-27b-it '{"inputs":"Explain Python","parameters":{"max_new_tokens":150}}' --pretty
```

**Note**: The Gemini connector provides access to Google's **Gemini API** models, not Gemma models. Available models include:
- `gemini-1.5-flash` - Fast and versatile (free tier)
- `gemini-2.0-flash` - Latest generation (free tier)  
- `gemini-2.5-flash` - Best price/performance
- `gemini-2.5-pro` - Most powerful model
- `gemini-1.5-pro` - Complex reasoning tasks

## License

MIT License
