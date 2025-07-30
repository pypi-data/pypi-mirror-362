import os
import json
import logging
import configparser
import requests
import glob
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        
        # Add function name and timestamp
        record.funcName = getattr(record, 'funcName', 'unknown')
        record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Format the message
        formatted = super().format(record)
        
        # Apply color to console output
        if hasattr(record, 'colored') and record.colored:
            return f"{log_color}{formatted}{Style.RESET_ALL}"
        return formatted


class APIConnector:
    """Represents an API connector configuration"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.name = config_data.get("name", "")
        self.host = config_data.get("host", "")
        self.port = config_data.get("port", 443 if config_data.get("protocol") == "https" else 80)
        self.protocol = config_data.get("protocol", "https")
        self.format = config_data.get("format", "json")
        self.requires_api_key = config_data.get("requires_api_key", True)
        
        # Store any additional custom attributes from the config
        for key, value in config_data.items():
            if not hasattr(self, key):
                setattr(self, key, value)
        
    @property
    def base_url(self) -> str:
        """Get the base URL for the API"""
        if self.port in [80, 443] and self.protocol in ["http", "https"]:
            return f"{self.protocol}://{self.host}"
        return f"{self.protocol}://{self.host}:{self.port}"


class APIJongler:
    """Main APIJongler class for managing multiple API keys and connections"""
    
    def __init__(self, api_connector_name: str, is_tor_enabled: Optional[bool] = False):
        """
        Initialize APIJongler
        
        Args:
            api_connector_name: Name of the API connector to use
            is_tor_enabled: Whether to use Tor for requests (optional)
        """
        self.api_connector_name = api_connector_name
        self.is_tor_enabled = is_tor_enabled
        self.api_connector = None
        self.current_api_key = None
        self.session = None
        self.lock_file_path = None
        
        # Set up logging
        self._setup_logging()
        
        # Connect to the API
        self._connect(api_connector_name, is_tor_enabled)
        
    def _setup_logging(self):
        """Set up logging configuration"""
        log_level = os.getenv('APIJONGLER_LOG_LEVEL', 'INFO').upper()
        log_format = '%(timestamp)s - %(funcName)s - %(levelname)s - %(message)s'
        
        # Create logger
        self.logger = logging.getLogger('APIJongler')
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(log_format)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler without colors
        log_dir = Path.home() / '.api_jongler' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / 'api_jongler.log'
        
        file_handler = logging.FileHandler(log_file)
        file_formatter = ColoredFormatter(log_format)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Add colored attribute for console output
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream.name == '<stderr>':
                handler.addFilter(lambda record: setattr(record, 'colored', True) or True)
        
    def _connect(self, api_connector_name: str, is_tor_enabled: bool):
        """
        Connect to the API service
        
        Args:
            api_connector_name: Name of the API connector
            is_tor_enabled: Whether to use Tor connection
        """
        self.logger.info(f"Connecting to API connector: {api_connector_name}")
        
        # Load API connector configuration
        self.api_connector = self._load_api_connector(api_connector_name)
        
        # Set up Tor connection if enabled
        if is_tor_enabled:
            self._setup_tor_connection()
        else:
            self.session = requests.Session()
        
        # Get available API keys and select one
        self._select_api_key()
        
        self.logger.info(f"Successfully connected to {api_connector_name}")
    
    def _load_api_connector(self, connector_name: str) -> APIConnector:
        """Load API connector configuration from JSON file"""
        # Get the package directory
        package_dir = Path(__file__).parent
        connector_file = package_dir / 'connectors' / f'{connector_name}.json'
        
        if not connector_file.exists():
            raise FileNotFoundError(f"API connector configuration not found: {connector_file}")
        
        try:
            with open(connector_file, 'r') as f:
                config_data = json.load(f)
            return APIConnector(config_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in connector file {connector_file}: {e}")
    
    def _setup_tor_connection(self):
        """Set up Tor connection for requests"""
        self.logger.info("Setting up Tor connection")
        
        self.session = requests.Session()
        
        # Configure Tor proxy (default Tor SOCKS proxy)
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        self.session.proxies.update(proxies)
        
        # Test Tor connection
        try:
            response = self.session.get('https://httpbin.org/ip', timeout=10)
            self.logger.info(f"Tor connection established. IP: {response.json().get('origin', 'unknown')}")
        except Exception as e:
            self.logger.warning(f"Could not verify Tor connection: {e}")
    
    def _get_lock_directory(self) -> Path:
        """Get the lock directory path"""
        lock_dir = Path.home() / '.api_jongler' / 'locks'
        lock_dir.mkdir(parents=True, exist_ok=True)
        return lock_dir
    
    def _get_config_file_path(self) -> str:
        """Get the configuration file path from environment variable"""
        config_path = os.getenv('APIJONGLER_CONFIG')
        if not config_path:
            raise ValueError("APIJONGLER_CONFIG environment variable not set")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        return config_path
    
    def _get_api_keys(self) -> Dict[str, str]:
        """Get API keys from configuration file"""
        config_path = self._get_config_file_path()
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if self.api_connector_name not in config:
            raise ValueError(f"No configuration section found for {self.api_connector_name}")
        
        return dict(config[self.api_connector_name])
    
    def _get_locked_and_error_keys(self) -> set:
        """Get set of API keys that are locked or have errors"""
        lock_dir = self._get_lock_directory()
        
        # Get locked keys
        lock_files = glob.glob(str(lock_dir / f"{self.api_connector_name}_*.lock"))
        locked_keys = {Path(f).stem.replace(f"{self.api_connector_name}_", "") for f in lock_files}
        
        # Get error keys
        error_files = glob.glob(str(lock_dir / f"{self.api_connector_name}_*.error"))
        error_keys = {Path(f).stem.replace(f"{self.api_connector_name}_", "") for f in error_files}
        
        unavailable_keys = locked_keys | error_keys
        
        if unavailable_keys:
            self.logger.debug(f"Unavailable keys: {unavailable_keys}")
        
        return unavailable_keys
    
    def _select_api_key(self):
        """Select an available API key and create lock file"""
        api_keys = self._get_api_keys()
        unavailable_keys = self._get_locked_and_error_keys()
        
        # Filter out unavailable keys
        available_keys = {k: v for k, v in api_keys.items() if k not in unavailable_keys}
        
        if not available_keys:
            raise RuntimeError(f"No available API keys for {self.api_connector_name}")
        
        # Select the first available key
        key_name = list(available_keys.keys())[0]
        self.current_api_key = available_keys[key_name]
        
        # Create lock file
        lock_dir = self._get_lock_directory()
        self.lock_file_path = lock_dir / f"{self.api_connector_name}_{key_name}.lock"
        
        with open(self.lock_file_path, 'w') as f:
            f.write(str(int(time.time())))
        
        self.logger.info(f"Selected API key: {key_name} (locked)")
    
    def request(self, method: str, endpoint: str, request: str) -> Tuple[str, int]:
        """
        Execute API request with raw string data
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: Relative path to append to base URL
            request: Request body as string
        
        Returns:
            Tuple of (response_text, status_code)
        """
        self.logger.info(f"Executing {method} request to {endpoint}")
        
        # Check if there's an error file for current API key
        lock_dir = self._get_lock_directory()
        key_name = self._get_current_key_name()
        error_file = lock_dir / f"{self.api_connector_name}_{key_name}.error"
        
        if error_file.exists():
            self.logger.error(f"API key {key_name} has error status, cannot proceed")
            raise RuntimeError(f"API key {key_name} is in error state")
        
        # Prepare request
        url = f"{self.api_connector.base_url}{endpoint}"
        headers = self._prepare_headers()
        
        # For Google/Gemini APIs, add API key as query parameter
        params = {}
        if self.api_connector.name in ['generativelanguage.googleapis.com', 'google'] and self.current_api_key:
            params['key'] = self.current_api_key
            # Remove Authorization header for Google APIs since they use query param
            if 'Authorization' in headers:
                del headers['Authorization']
        
        try:
            # Make the request
            response = self.session.request(
                method=method.upper(),
                url=url,
                data=request,
                headers=headers,
                params=params,
                timeout=30
            )
            
            # Check for authentication errors
            if response.status_code in [401, 403]:
                self.logger.error(f"Authentication error (status {response.status_code}), marking key as error")
                self._create_error_file(key_name)
                raise RuntimeError(f"Authentication failed with status {response.status_code}")
            
            self.logger.info(f"Request successful, status code: {response.status_code}")
            return response.text, response.status_code
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise RuntimeError(f"Request failed: {e}")
    
    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare request headers including API key"""
        headers = {
            'Content-Type': 'application/json' if self.api_connector.format == 'json' else 'application/xml',
        }
        
        if self.api_connector.requires_api_key and self.current_api_key:
            # Check if connector specifies custom auth header
            if hasattr(self.api_connector, 'api_key_header') and self.api_connector.api_key_header:
                header_name = self.api_connector.api_key_header
                prefix = getattr(self.api_connector, 'api_key_prefix', '')
                headers[header_name] = f'{prefix}{self.current_api_key}'
            else:
                # Default to Bearer token authentication
                headers['Authorization'] = f'Bearer {self.current_api_key}'
        
        return headers
    
    def _get_current_key_name(self) -> str:
        """Get the current API key name from lock file path"""
        if not self.lock_file_path:
            raise RuntimeError("No lock file path available")
        
        lock_filename = self.lock_file_path.stem
        return lock_filename.replace(f"{self.api_connector_name}_", "")
    
    def _create_error_file(self, key_name: str):
        """Create error file for the given API key"""
        lock_dir = self._get_lock_directory()
        error_file = lock_dir / f"{self.api_connector_name}_{key_name}.error"
        
        with open(error_file, 'w') as f:
            f.write(str(int(time.time())))
        
        self.logger.warning(f"Created error file for key: {key_name}")
    
    def _disconnect(self):
        """Disconnect and cleanup resources"""
        self.logger.info("Disconnecting from API")
        
        # Remove lock file
        if self.lock_file_path and self.lock_file_path.exists():
            try:
                self.lock_file_path.unlink()
                self.logger.info(f"Removed lock file: {self.lock_file_path}")
            except Exception as e:
                self.logger.error(f"Failed to remove lock file: {e}")
        
        # Close session
        if self.session:
            self.session.close()

    def requestJSON(self, endpoint: str, method: str = 'POST', data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request with automatic JSON handling
        
        Args:
            endpoint: API endpoint (relative path)
            method: HTTP method (default: POST)
            data: Request data as dictionary (will be JSON-encoded)
        
        Returns:
            Response as dictionary
        """
        import json as json_lib
        
        # Convert data to JSON string if provided
        if data is not None:
            request_body = json_lib.dumps(data)
        else:
            request_body = ""
        
        # Use the existing request method
        response_text, status_code = self.request(method, endpoint, request_body)
        
        # Try to parse as JSON
        try:
            return json_lib.loads(response_text)
        except json_lib.JSONDecodeError:
            # Return as plain text if not valid JSON
            return {"text": response_text, "status_code": status_code}

    # Backward compatibility aliases
    def run(self, method: str, endpoint: str, request: str) -> Tuple[str, int]:
        """
        DEPRECATED: Use request() instead. This method will be removed in a future version.
        """
        import warnings
        warnings.warn("run() is deprecated, use request() instead", DeprecationWarning, stacklevel=2)
        return self.request(method, endpoint, request)
    
    def make_request(self, endpoint: str, method: str = 'POST', data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        DEPRECATED: Use requestJSON() instead. This method will be removed in a future version.
        """
        import warnings
        warnings.warn("make_request() is deprecated, use requestJSON() instead", DeprecationWarning, stacklevel=2)
        return self.requestJSON(endpoint, method, data)

    def __del__(self):
        """Destructor - cleanup resources"""
        self._disconnect()
    
    @staticmethod
    def cleanUp(api_connector: Optional[str] = None):
        """
        Clean up lock and error files
        
        Args:
            api_connector: Specific API connector to clean up, or None for all
        """
        logger = logging.getLogger('APIJongler')
        lock_dir = Path.home() / '.api_jongler' / 'locks'
        
        if not lock_dir.exists():
            logger.info("No lock directory found, nothing to clean up")
            return
        
        if api_connector:
            pattern = f"{api_connector}_*"
            logger.info(f"Cleaning up files for API connector: {api_connector}")
        else:
            pattern = "*"
            logger.info("Cleaning up all lock and error files")
        
        # Remove lock files
        lock_files = glob.glob(str(lock_dir / f"{pattern}.lock"))
        for lock_file in lock_files:
            try:
                os.unlink(lock_file)
                logger.info(f"Removed lock file: {Path(lock_file).name}")
            except Exception as e:
                logger.error(f"Failed to remove lock file {lock_file}: {e}")
        
        # Remove error files
        error_files = glob.glob(str(lock_dir / f"{pattern}.error"))
        for error_file in error_files:
            try:
                os.unlink(error_file)
                logger.info(f"Removed error file: {Path(error_file).name}")
            except Exception as e:
                logger.error(f"Failed to remove error file {error_file}: {e}")
        
        removed_count = len(lock_files) + len(error_files)
        logger.info(f"Cleanup completed. Removed {removed_count} files.")
