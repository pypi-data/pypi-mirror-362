"""
Test runner for API Jongler
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import test modules
from tests.test_api_jongler import *

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
