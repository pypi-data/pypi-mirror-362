"""
Example usage of APIJongler with Gemma models via Hugging Face Inference API
"""

from api_jongler import APIJongler
import json

# Initialize with Gemma connector
jongler = APIJongler(
    config_file='APIJongler.ini',
    connector='api-inference.huggingface.co',
    lock_file_dir='./locks',
    error_file_dir='./errors'
)

# Example 1: Basic text generation with Gemma 2 9B
try:
    # Hugging Face Inference API expects the prompt in 'inputs' field
    response = jongler.requestJSON(
        endpoint='models/google/gemma-2-9b-it',
        method='POST',
        data={
            "inputs": "What is the capital of France?",
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
    )
    
    print("Gemma 2 9B Response:")
    print(json.dumps(response, indent=2))
    
except Exception as e:
    print(f"Error: {e}")

# Example 2: Using Gemma 2 27B for a more complex task
try:
    prompt = """You are a helpful assistant. Please explain the concept of machine learning in simple terms that a beginner can understand."""
    
    response = jongler.requestJSON(
        endpoint='models/google/gemma-2-27b-it',
        method='POST',
        data={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.8,
                "do_sample": True,
                "top_p": 0.9
            }
        }
    )
    
    print("\nGemma 2 27B Response:")
    print(json.dumps(response, indent=2))
    
except Exception as e:
    print(f"Error: {e}")

# Example 3: Conversation with Gemma using chat format
try:
    # Note: Some Gemma models support chat format, others expect simple text
    conversation = "Human: What are the benefits of renewable energy?\n\nAssistant:"
    
    response = jongler.requestJSON(
        endpoint='models/google/gemma-1.1-7b-it',
        method='POST',
        data={
            "inputs": conversation,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.6,
                "stop": ["Human:", "\n\n"]
            }
        }
    )
    
    print("\nGemma 1.1 7B Conversation Response:")
    print(json.dumps(response, indent=2))
    
except Exception as e:
    print(f"Error: {e}")

print("\nNote: You need a Hugging Face API token to use this connector.")
print("Get one at: https://huggingface.co/settings/tokens")
print("Add it to your APIJongler.ini under [api-inference.huggingface.co] section as api_key_1, api_key_2, etc.")
