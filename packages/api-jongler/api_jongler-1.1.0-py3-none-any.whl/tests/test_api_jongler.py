import unittest
import os
import tempfile
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api_jongler import APIJongler
from api_jongler.api_jongler import APIConnector


class TestAPIConnector(unittest.TestCase):
    """Test APIConnector class"""
    
    def test_api_connector_initialization(self):
        """Test APIConnector initialization with different configurations"""
        
        # Test basic configuration
        config_data = {
            "name": "test",
            "host": "api.test.com",
            "protocol": "https",
            "format": "json",
            "requires_api_key": True
        }
        
        connector = APIConnector(config_data)
        
        self.assertEqual(connector.name, "test")
        self.assertEqual(connector.host, "api.test.com")
        self.assertEqual(connector.port, 443)  # Default HTTPS port
        self.assertEqual(connector.protocol, "https")
        self.assertEqual(connector.format, "json")
        self.assertTrue(connector.requires_api_key)
        self.assertEqual(connector.base_url, "https://api.test.com")
    
    def test_api_connector_custom_port(self):
        """Test APIConnector with custom port"""
        
        config_data = {
            "name": "test",
            "host": "api.test.com",
            "port": 8080,
            "protocol": "http",
            "format": "xml",
            "requires_api_key": False
        }
        
        connector = APIConnector(config_data)
        
        self.assertEqual(connector.port, 8080)
        self.assertEqual(connector.protocol, "http")
        self.assertEqual(connector.format, "xml")
        self.assertFalse(connector.requires_api_key)
        self.assertEqual(connector.base_url, "http://api.test.com:8080")


class TestAPIJongler(unittest.TestCase):
    """Test APIJongler class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
        
        # Write test configuration
        config_content = """[generativelanguage.googleapis.com]
key1 = test-gemini-key-1
key2 = test-gemini-key-2

[api-inference.huggingface.co]
key1 = test-gemma-key-1
key2 = test-gemma-key-2

[httpbin.org]
key1 = test-key-1
key2 = test-key-2
key3 = test-key-3
"""
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        # Set environment variable
        os.environ['APIJONGLER_CONFIG'] = str(self.config_file)
        os.environ['APIJONGLER_LOG_LEVEL'] = 'ERROR'  # Reduce log noise during tests
    
    def tearDown(self):
        """Clean up test environment"""
        # Clean up any lock/error files
        APIJongler.cleanUp()
        
        # Remove temporary files
        if self.config_file.exists():
            self.config_file.unlink()
        
        # Remove temp directory
        Path(self.temp_dir).rmdir()
    
    def test_missing_config_file(self):
        """Test behavior when config file is missing"""
        os.environ['APIJONGLER_CONFIG'] = '/nonexistent/config.ini'
        
        with self.assertRaises(FileNotFoundError):
            APIJongler("httpbin.org")
    
    def test_missing_config_env_var(self):
        """Test behavior when config environment variable is not set"""
        if 'APIJONGLER_CONFIG' in os.environ:
            del os.environ['APIJONGLER_CONFIG']
        
        with self.assertRaises(ValueError):
            APIJongler("httpbin.org")
    
    def test_missing_connector_file(self):
        """Test behavior when connector file doesn't exist"""
        # Reset config
        os.environ['APIJONGLER_CONFIG'] = str(self.config_file)
        
        with self.assertRaises(FileNotFoundError):
            APIJongler("nonexistent_connector")
    
    def test_api_key_selection(self):
        """Test API key selection and locking"""
        jongler = APIJongler("httpbin.org")
        
        # Should have selected an API key
        self.assertIsNotNone(jongler.current_api_key)
        self.assertIn(jongler.current_api_key, ["test-key-1", "test-key-2", "test-key-3"])
        
        # Should have created a lock file
        self.assertIsNotNone(jongler.lock_file_path)
        self.assertTrue(jongler.lock_file_path.exists())
        
        # Clean up
        del jongler
    
    def test_multiple_instances_key_rotation(self):
        """Test that multiple instances use different keys"""
        jongler1 = APIJongler("httpbin.org")
        jongler2 = APIJongler("httpbin.org")
        
        # Should use different keys
        self.assertNotEqual(jongler1.current_api_key, jongler2.current_api_key)
        
        # Should have different lock files
        self.assertNotEqual(jongler1.lock_file_path, jongler2.lock_file_path)
        
        # Clean up
        del jongler1
        del jongler2
    
    def test_cleanup_function(self):
        """Test cleanup functionality"""
        # Create some instances
        jongler1 = APIJongler("httpbin.org")
        jongler2 = APIJongler("httpbin.org")
        
        lock_files_before = list(jongler1._get_lock_directory().glob("httpbin.org_*.lock"))
        self.assertGreaterEqual(len(lock_files_before), 2)
        
        # Clean up specific connector
        APIJongler.cleanUp("httpbin.org")
        
        lock_files_after = list(jongler1._get_lock_directory().glob("httpbin.org_*.lock"))
        self.assertEqual(len(lock_files_after), 0)
        
        # Clean up instances (should not fail even though lock files are gone)
        del jongler1
        del jongler2
    
    def test_gemini_connector_loading(self):
        """Test that Gemini connector loads correctly"""
        try:
            jongler = APIJongler("generativelanguage.googleapis.com")
            
            # Should have loaded the connector
            self.assertEqual(jongler.api_connector.name, "generativelanguage.googleapis.com")
            self.assertEqual(jongler.api_connector.host, "generativelanguage.googleapis.com")
            self.assertEqual(jongler.api_connector.port, 443)
            self.assertEqual(jongler.api_connector.protocol, "https")
            self.assertTrue(jongler.api_connector.requires_api_key)
            
            # Should have selected an API key
            self.assertIsNotNone(jongler.current_api_key)
            self.assertIn(jongler.current_api_key, ["test-gemini-key-1", "test-gemini-key-2"])
            
            del jongler
            
        except Exception as e:
            self.fail(f"Gemini connector test failed: {e}")

    def test_gemma_connector_loading(self):
        """Test that Gemma connector loads correctly"""
        try:
            jongler = APIJongler("api-inference.huggingface.co")
            
            # Should have loaded the connector
            self.assertEqual(jongler.api_connector.name, "api-inference.huggingface.co")
            self.assertEqual(jongler.api_connector.host, "api-inference.huggingface.co")
            self.assertEqual(jongler.api_connector.port, 443)
            self.assertEqual(jongler.api_connector.protocol, "https")
            self.assertTrue(jongler.api_connector.requires_api_key)
            
            # Should have custom auth header
            self.assertEqual(getattr(jongler.api_connector, 'api_key_header', None), "Authorization")
            self.assertEqual(getattr(jongler.api_connector, 'api_key_prefix', None), "Bearer ")
            
            # Should have selected an API key
            self.assertIsNotNone(jongler.current_api_key)
            self.assertIn(jongler.current_api_key, ["test-gemma-key-1", "test-gemma-key-2"])
            
            del jongler
            
        except Exception as e:
            self.fail(f"Gemma connector test failed: {e}")

    def test_http_request(self):
        """Test making actual HTTP request"""
        jongler = APIJongler("httpbin.org")
        
        try:
            response, status_code = jongler.request(
                method="GET",
                endpoint="/json",
                request=""
            )
            
            self.assertEqual(status_code, 200)
            self.assertIsInstance(response, str)
            
            # Should be valid JSON
            json.loads(response)
            
        except Exception as e:
            self.fail(f"HTTP request failed: {e}")
        
        finally:
            del jongler


if __name__ == '__main__':
    unittest.main()
