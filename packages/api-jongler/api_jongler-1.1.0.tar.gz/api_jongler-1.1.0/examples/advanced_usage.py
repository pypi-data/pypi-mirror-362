#!/usr/bin/env python3
"""
Advanced usage example for APIJongler with multiple connectors and Tor
"""

import os
import sys
import json
import time
from pathlib import Path

# Add the parent directory to the path so we can import api_jongler
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler


def test_multiple_keys():
    """Test multiple API key rotation"""
    print("\n=== Testing Multiple API Key Rotation ===")
    
    # Create multiple instances to test key rotation
    jonglers = []
    
    try:
        for i in range(3):
            print(f"\nCreating APIJongler instance {i+1}...")
            jongler = APIJongler("httpbin.org", is_tor_enabled=False)
            jonglers.append(jongler)
            
            # Make a request
            response, status_code = jongler.request(
                method="GET",
                endpoint="/headers",
                request=""
            )
            
            print(f"Instance {i+1} - Status: {status_code}")
            
        print("\nAll instances created successfully - key rotation working!")
        
    except Exception as e:
        print(f"Error during multiple key test: {e}")
    
    finally:
        # Clean up all instances
        for jongler in jonglers:
            del jongler


def test_tor_connection():
    """Test Tor connection (requires Tor to be running)"""
    print("\n=== Testing Tor Connection ===")
    
    try:
        print("Attempting to connect through Tor...")
        print("Note: This requires Tor to be installed and running on port 9050")
        
        jongler = APIJongler("httpbin.org", is_tor_enabled=True)
        
        # Get IP address to verify Tor connection
        response, status_code = jongler.request(
            method="GET",
            endpoint="/ip",
            request=""
        )
        
        if status_code == 200:
            ip_data = json.loads(response)
            print(f"Request successful through Tor!")
            print(f"IP Address: {ip_data.get('origin', 'unknown')}")
        else:
            print(f"Request failed with status: {status_code}")
        
        del jongler
        
    except Exception as e:
        print(f"Tor connection failed: {e}")
        print("Make sure Tor is installed and running on port 9050")


def test_error_handling():
    """Test error handling and error file creation"""
    print("\n=== Testing Error Handling ===")
    
    try:
        # This will test with a non-existent connector
        try:
            jongler = APIJongler("nonexistent", is_tor_enabled=False)
        except FileNotFoundError as e:
            print(f"✓ Correctly caught missing connector: {e}")
        
        # Test with missing config
        original_config = os.environ.get('APIJONGLER_CONFIG')
        os.environ['APIJONGLER_CONFIG'] = '/nonexistent/path'
        
        try:
            jongler = APIJongler("httpbin.org", is_tor_enabled=False)
        except FileNotFoundError as e:
            print(f"✓ Correctly caught missing config: {e}")
        finally:
            if original_config:
                os.environ['APIJONGLER_CONFIG'] = original_config
        
        print("Error handling tests completed!")
        
    except Exception as e:
        print(f"Unexpected error during error handling test: {e}")


def main():
    """Advanced example of using APIJongler"""
    
    # Set up configuration
    config_path = Path(__file__).parent.parent / "APIJongler.ini.example"
    os.environ['APIJONGLER_CONFIG'] = str(config_path)
    os.environ['APIJONGLER_LOG_LEVEL'] = 'DEBUG'
    
    print("=== APIJongler Advanced Example ===")
    
    # Test different scenarios
    test_multiple_keys()
    test_tor_connection()
    test_error_handling()
    
    # Final cleanup
    print("\n=== Final Cleanup ===")
    APIJongler.cleanUp()
    
    print("\nAdvanced example completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
