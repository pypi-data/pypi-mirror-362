#!/usr/bin/env python3
"""
Basic usage example for APIJongler
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import api_jongler
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler


def main():
    """Basic example of using APIJongler"""
    
    # Set up configuration (you would normally set this as an environment variable)
    config_path = Path(__file__).parent.parent / "APIJongler.ini.example"
    os.environ['APIJONGLER_CONFIG'] = str(config_path)
    
    # Optional: Set logging level
    os.environ['APIJONGLER_LOG_LEVEL'] = 'INFO'
    
    print("=== APIJongler Basic Example ===")
    
    try:
        # Test with httpbin (doesn't require real API keys)
        print("\n1. Testing with httpbin connector...")
        jongler = APIJongler("httpbin.org", is_tor_enabled=False)
        
        # Make a simple GET request
        response, status_code = jongler.request(
            method="GET",
            endpoint="/json",
            request=""
        )
        
        print(f"Response Status: {status_code}")
        print(f"Response Preview: {response[:200]}...")
        
        # Clean up
        del jongler
        
        print("\n2. Testing cleanup functionality...")
        APIJongler.cleanUp("httpbin.org")
        
        print("\nExample completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
