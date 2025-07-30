#!/usr/bin/env python3
"""
Comparison example showing the difference between request() and requestJSON() methods
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import api_jongler
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler


def main():
    """Compare request() vs requestJSON() methods"""
    print("=== APIJongler Method Comparison ===")
    
    # Set up configuration
    config_path = Path(__file__).parent.parent / "APIJongler.ini.example"
    os.environ['APIJONGLER_CONFIG'] = str(config_path)
    os.environ['APIJONGLER_LOG_LEVEL'] = 'WARNING'  # Reduce log noise
    
    try:
        # Using httpbin for testing (doesn't require real API keys)
        jongler = APIJongler("httpbin.org", is_tor_enabled=False)
        
        print("\n1. Using request() method (low-level, raw strings):")
        print("   - Input: Raw JSON string")
        print("   - Output: (response_text, status_code) tuple")
        
        # Example with request() - low-level method
        response_text, status_code = jongler.request(
            method="POST",
            endpoint="/post",
            request='{"test": "data", "number": 42}'
        )
        
        print(f"   Status Code: {status_code}")
        print(f"   Response Type: {type(response_text)}")
        print(f"   Raw Response: {response_text[:100]}...")
        
        # You need to parse JSON manually
        response_data = json.loads(response_text)
        print(f"   Parsed Data: {response_data['json']}")
        
        print("\n2. Using requestJSON() method (high-level, automatic JSON):")
        print("   - Input: Python dictionary")
        print("   - Output: Parsed dictionary")
        
        # Example with requestJSON() - high-level method
        response_data = jongler.requestJSON(
            endpoint="/post",
            method="POST",
            data={"test": "data", "number": 42}
        )
        
        print(f"   Response Type: {type(response_data)}")
        print(f"   Direct Access: {response_data['json']}")
        
        print("\n3. Summary:")
        print("   ✓ request() - For raw control and non-JSON APIs")
        print("   ✓ requestJSON() - For JSON APIs (recommended)")
        
        # Clean up
        del jongler
        
        print("\n✅ Method comparison completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
