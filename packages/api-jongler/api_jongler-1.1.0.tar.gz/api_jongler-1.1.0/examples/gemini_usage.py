#!/usr/bin/env python3
"""
Example usage of APIJongler with Google Gemini API
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import api_jongler
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler


def example_text_generation():
    """Example: Generate text using Gemini Flash (free tier)"""
    print("=== Google Gemini Text Generation Example ===")
    
    try:
        # Initialize with Gemini connector
        jongler = APIJongler("generativelanguage.googleapis.com", is_tor_enabled=False)
        
        # Prepare the request for Gemini 1.5 Flash (free tier model)
        request_data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Write a short story about a helpful AI assistant in exactly 3 sentences."
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        # Make the API call to Gemini 1.5 Flash
        response, status_code = jongler.request(
            method="POST",
            endpoint="/v1beta/models/gemini-1.5-flash:generateContent",
            request=json.dumps(request_data)
        )
        
        print(f"Status Code: {status_code}")
        
        if status_code == 200:
            response_data = json.loads(response)
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                text_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Generated Text: {text_content}")
                
                # Show token usage if available
                if "usageMetadata" in response_data:
                    usage = response_data["usageMetadata"]
                    print(f"Token Usage - Prompt: {usage.get('promptTokenCount', 'N/A')}, "
                          f"Response: {usage.get('candidatesTokenCount', 'N/A')}, "
                          f"Total: {usage.get('totalTokenCount', 'N/A')}")
            else:
                print("No content generated")
        else:
            print(f"Error: {response}")
        
        # Clean up
        del jongler
        
    except Exception as e:
        print(f"Error: {e}")


def example_chat_conversation():
    """Example: Multi-turn chat conversation with Gemini"""
    print("\n=== Google Gemini Chat Example ===")
    
    try:
        jongler = APIJongler("generativelanguage.googleapis.com", is_tor_enabled=False)
        
        # Simulate a multi-turn conversation
        conversation_history = [
            {
                "role": "user",
                "parts": [{"text": "Hello! Can you help me understand what Python is?"}]
            },
            {
                "role": "model",
                "parts": [{"text": "Hello! I'd be happy to help you understand Python. Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, artificial intelligence, automation, and many other applications. Would you like to know more about any specific aspect of Python?"}]
            },
            {
                "role": "user",
                "parts": [{"text": "What makes Python good for beginners?"}]
            }
        ]
        
        request_data = {
            "contents": conversation_history,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300
            }
        }
        
        # Use Gemini 2.0 Flash (also free tier)
        response, status_code = jongler.request(
            method="POST",
            endpoint="/v1beta/models/gemini-2.0-flash:generateContent",
            request=json.dumps(request_data)
        )
        
        print(f"Status Code: {status_code}")
        
        if status_code == 200:
            response_data = json.loads(response)
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                text_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Gemini Response: {text_content}")
            else:
                print("No response generated")
        else:
            print(f"Error: {response}")
        
        del jongler
        
    except Exception as e:
        print(f"Error: {e}")


def example_with_system_instruction():
    """Example: Using system instructions with Gemini"""
    print("\n=== Google Gemini System Instruction Example ===")
    
    try:
        jongler = APIJongler("generativelanguage.googleapis.com", is_tor_enabled=False)
        
        request_data = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": "You are a helpful coding assistant. Always provide concise, practical examples when explaining programming concepts."
                    }
                ]
            },
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Explain how to create a simple function in Python that adds two numbers."
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 250
            }
        }
        
        response, status_code = jongler.request(
            method="POST",
            endpoint="/v1beta/models/gemini-1.5-flash:generateContent",
            request=json.dumps(request_data)
        )
        
        print(f"Status Code: {status_code}")
        
        if status_code == 200:
            response_data = json.loads(response)
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                text_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Coding Assistant Response: {text_content}")
            else:
                print("No response generated")
        else:
            print(f"Error: {response}")
        
        del jongler
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to run all examples"""
    
    # Set up configuration
    config_path = Path(__file__).parent.parent / "APIJongler.ini.example"
    os.environ['APIJONGLER_CONFIG'] = str(config_path)
    os.environ['APIJONGLER_LOG_LEVEL'] = 'INFO'
    
    print("Google Gemini API Examples")
    print("=" * 50)
    print("Note: These examples use the free tier Gemini models:")
    print("- gemini-1.5-flash: Fast and versatile, good for most tasks")
    print("- gemini-2.0-flash: Latest generation with enhanced capabilities")
    print()
    print("To use these examples with real API keys:")
    print("1. Get your free Gemini API key from: https://aistudio.google.com/app/apikey")
    print("2. Add your keys to the [gemini] section in your config file")
    print("3. Set APIJONGLER_CONFIG environment variable to your config file path")
    print()
    
    try:
        # Run examples
        example_text_generation()
        example_chat_conversation() 
        example_with_system_instruction()
        
        print("\n=== Examples completed! ===")
        print("Free tier limits for Gemini API:")
        print("- 15 requests per minute")
        print("- 1 million tokens per minute")
        print("- 1,500 requests per day")
        print("For higher limits, consider upgrading to a paid plan.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have valid Gemini API keys in your config")
        print("2. Check that APIJONGLER_CONFIG points to your config file")
        print("3. Verify your internet connection")
        print("4. Check if you've exceeded free tier rate limits")


if __name__ == "__main__":
    main()
