#!/usr/bin/env python3
"""
Command-line interface for APIJongler
"""

import argparse
import sys
import os
import json
from pathlib import Path

# Add parent directory to path for development
if __name__ == "__main__" and "site-packages" not in __file__:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="APIJongler - Middleware for managing multiple API keys",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use Google Gemini free tier
  python -m api_jongler.cli generativelanguage.googleapis.com POST /v1beta/models/gemini-1.5-flash:generateContent '{"contents":[{"parts":[{"text":"Hello"}]}]}'

  # Use Gemma models via Hugging Face
  python -m api_jongler.cli api-inference.huggingface.co POST /models/google/gemma-2-9b-it '{"inputs":"What is machine learning?","parameters":{"max_new_tokens":100}}'

  # Clean up lock files for Gemini
  python -m api_jongler.cli --cleanup generativelanguage.googleapis.com

  # Clean up all lock files
  python -m api_jongler.cli --cleanup-all
        """
    )
    
    parser.add_argument(
        "connector",
        nargs="?",
        help="API connector name (e.g., generativelanguage.googleapis.com, api-inference.huggingface.co)"
    )
    
    parser.add_argument(
        "method",
        nargs="?",
        help="HTTP method (GET, POST, PUT, DELETE, etc.)"
    )
    
    parser.add_argument(
        "endpoint",
        nargs="?",
        help="API endpoint path (e.g., /v1/chat/completions)"
    )
    
    parser.add_argument(
        "data",
        nargs="?",
        default="",
        help="Request body data (JSON string for POST/PUT requests)"
    )
    
    parser.add_argument(
        "--tor",
        action="store_true",
        help="Use Tor connection for the request"
    )
    
    parser.add_argument(
        "--cleanup",
        metavar="CONNECTOR",
        help="Clean up lock and error files for specified connector"
    )
    
    parser.add_argument(
        "--cleanup-all",
        action="store_true",
        help="Clean up all lock and error files"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file (overrides APIJONGLER_CONFIG env var)"
    )
    
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON responses"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    os.environ['APIJONGLER_LOG_LEVEL'] = args.log_level
    
    # Set config file if provided
    if args.config:
        os.environ['APIJONGLER_CONFIG'] = args.config
    
    try:
        # Handle cleanup operations
        if args.cleanup_all:
            print("Cleaning up all lock and error files...")
            APIJongler.cleanUp()
            print("Cleanup completed.")
            return 0
        
        if args.cleanup:
            print(f"Cleaning up lock and error files for {args.cleanup}...")
            APIJongler.cleanUp(args.cleanup)
            print("Cleanup completed.")
            return 0
        
        # Validate required arguments for API calls
        if not all([args.connector, args.method, args.endpoint]):
            parser.error("connector, method, and endpoint are required for API calls")
        
        # Make API call
        print(f"Making {args.method} request to {args.connector}{args.endpoint}")
        if args.tor:
            print("Using Tor connection...")
        
        jongler = APIJongler(args.connector, is_tor_enabled=args.tor)
        
        response, status_code = jongler.request(
            method=args.method,
            endpoint=args.endpoint,
            request=args.data
        )
        
        print(f"\nStatus Code: {status_code}")
        print("Response:")
        
        # Pretty print JSON if requested and response is JSON
        if args.pretty:
            try:
                parsed = json.loads(response)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(response)
        else:
            print(response)
        
        # Cleanup
        del jongler
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
