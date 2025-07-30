import os
import logging
import requests
from typing import Optional, Dict, Any
from .exceptions import KiteError, KiteAuthenticationError, KiteNetworkError, KiteNotFoundError
from .util import (
    openapi_to_description,
    find_matching_endpoint,
    extract_input_fields_from_schema,
    extract_response_fields_from_schema,
    validate_payload_against_openapi
)

class KiteClient:
    """
    Kite SDK Client for interacting with Kite backend and blockchain layer.
    """

    DEFAULT_API_BASE_URL = "https://neo.prod.gokite.ai"  # Example base URL, replace with actual if different

    @classmethod
    def enable_verbose_logging(cls):
        """
        Enable verbose logging globally for all KiteClient instances.
        Useful for debugging in Python shell or interactive environments.
        """
        # Set root logger level to DEBUG so our messages show up
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Add a console handler to root logger if none exists
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
            
        print("Global verbose logging enabled for KiteClient")

    @classmethod  
    def disable_verbose_logging(cls):
        """
        Disable verbose logging globally.
        """
        logging.getLogger().setLevel(logging.WARNING)
        print("Global verbose logging disabled for KiteClient")

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        verbose: bool = False
    ):
        self.api_key = api_key or os.environ.get("KITE_API_KEY")
        if not self.api_key:
            raise KiteAuthenticationError("Missing KITE_API_KEY")

        self.base_url = base_url or self.DEFAULT_API_BASE_URL
        self.verbose = verbose
        
        # Set up logging for verbose mode
        self.logger = logging.getLogger(f"KiteClient.{id(self)}")
        if self.verbose:
            # Remove any existing handlers to avoid duplicates
            self.logger.handlers.clear()
            
            # Create a console handler that will show in Python shell
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            
            # Create formatter
            formatter = logging.Formatter('%(asctime)s - KiteClient - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.DEBUG)
            
            # Prevent propagation to avoid duplicate messages
            self.logger.propagate = False
            
            self.logger.warning("VERBOSE MODE ENABLED: This will log detailed information including HTTP requests, responses, and parameters. This may leak sensitive credentials and should only be used in test environments.")
        else:
            self.logger.addHandler(logging.NullHandler())
            self.logger.setLevel(logging.WARNING)

        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": f"{self.api_key}",
            "Content-Type": "application/json"
        })
        # cache service details
        self._service_details = {}

    def _log_method_call(self, method_name: str, **kwargs):
        """Log method call with parameters if verbose mode is enabled"""
        if self.verbose:
            self.logger.debug(f"Method called: {method_name}")
            for key, value in kwargs.items():
                # Mask sensitive information
                if 'api_key' in key.lower() or 'token' in key.lower() or 'password' in key.lower():
                    self.logger.debug(f"  {key}: [MASKED]")
                else:
                    self.logger.debug(f"  {key}: {value}")

    def _log_http_request(self, method: str, url: str, headers: dict = None, body: dict = None):
        """Log HTTP request details if verbose mode is enabled"""
        if self.verbose:
            self.logger.debug(f"HTTP {method} Request to: {url}")
            if headers:
                masked_headers = {}
                for key, value in headers.items():
                    if 'api' in key.lower() or 'auth' in key.lower() or 'key' in key.lower() or 'token' in key.lower():
                        masked_headers[key] = '[MASKED]'
                    else:
                        masked_headers[key] = value
                self.logger.debug(f"  Headers: {masked_headers}")
            if body:
                self.logger.debug(f"  Body: {body}")

    def _log_http_response(self, response: requests.Response):
        """Log HTTP response details if verbose mode is enabled"""
        if self.verbose:
            self.logger.debug(f"HTTP Response: {response.status_code}")
            self.logger.debug(f"  Response headers: {dict(response.headers)}")
            try:
                response_data = response.json()
                self.logger.debug(f"  Response body: {response_data}")
            except Exception: 
                self.logger.debug(f"  Response text: {response.text}")

    def make_payment(self, to_address: str, amount: float) -> str:
        """Make on-chain payment"""
        raise NotImplementedError("MakePayment is not implemented yet")

    def _get_service_details(self, service_id: str) -> Dict[str, Any]:
        """
        Fetch service details from /v1/asset endpoint with caching.

        Args:
            service_id: The service ID to fetch details for

        Returns:
            Dictionary containing service details including service_url and schema
        """
        self._log_method_call("_get_service_details", service_id=service_id)
        
        # try load from cache
        if service_id in self._service_details:
            if self.verbose:
                self.logger.debug(f"Service details for {service_id} found in cache")
            return self._service_details[service_id]

        url = f"{self.base_url}/v1/asset?"
        if service_id.startswith("agent_") or service_id.startswith("tool_") or service_id.startswith("dataset_"):
            url += f"id={service_id}"
        else:
            url += f"name={service_id}"

        self._log_http_request("GET", url, headers=dict(self.session.headers))
        
        try:
            response = self.session.get(url)
            self._log_http_response(response)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Network error in _get_service_details: {e}")
            raise KiteNetworkError(e)

        result = self._handle_response(response)
        if not result.get("data"):
            raise KiteError(f"Invalid response (status {response.status_code}): {result.get('error', response.text)}")

        # Cache service response
        self._service_details[result["data"]["id"]] = result["data"]
        if self.verbose:
            self.logger.debug(f"Cached service details for {result['data']['id']}")
        return result["data"]

    def load_service_description(self, service_id: str) -> str:
        """Load service description from cached service details"""
        self._log_method_call("load_service_description", service_id=service_id)
        service_details = self._get_service_details(service_id)
        result = service_details.get("description")
        if self.verbose:
            self.logger.debug(f"Returning description: {result}")
        return result

    def load_service_input_fields(self, service_id: str) -> Dict[str, str]:
        """
        Load service input fields from OpenAPI schema.

        Args:
            service_id: The service ID to get input fields for

        Returns:
            Dictionary mapping parameter names to their data types.
            For GET methods, returns empty dict.
            For POST/PUT/PATCH methods, returns dict of request body parameters.
        """
        self._log_method_call("load_service_input_fields", service_id=service_id)
        service_details = self._get_service_details(service_id)
        schema = service_details.get("schema")
        service_url = service_details.get("service_url")

        if not schema or not service_url:
            if self.verbose:
                self.logger.debug("No schema or service_url found, returning empty dict")
            return {}

        try:
            result = extract_input_fields_from_schema(schema, service_url)
            if self.verbose:
                self.logger.debug(f"Extracted input fields: {result}")
            return result
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"Error extracting input fields from schema: {e}")
            print(f"Warning: Error extracting input fields from schema: {e}")
            return {}

    def load_service_response_fields(self, service_id: str) -> Dict[str, str]:
        """
        Load service response fields from OpenAPI schema.

        Args:
            service_id: The service ID to get response fields for

        Returns:
            Dictionary mapping parameter names to their data types.
        """
        self._log_method_call("load_service_response_fields", service_id=service_id)
        service_details = self._get_service_details(service_id)
        schema = service_details.get("schema")
        service_url = service_details.get("service_url")

        if not schema or not service_url:
            if self.verbose:
                self.logger.debug("No schema or service_url found, returning empty dict")
            return {}

        try:
            result = extract_response_fields_from_schema(schema, service_url)
            if self.verbose:
                self.logger.debug(f"Extracted response fields: {result}")
            return result
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"Error extracting response fields from schema: {e}")
            print(f"Warning: Error extracting response fields from schema: {e}")
            return {}

    def call_service(self, service_id: str, payload: dict, headers: dict = {}) -> dict:
        """
        Call a service with payload validation against OpenAPI schema.

        Args:
            service_id: The service ID to call
            payload: The payload to send to the service
            headers: Additional headers to include in the request

        Returns:
            Response from the service
        """
        self._log_method_call("call_service", service_id=service_id, payload=payload, headers=headers)
        
        # Get service details including service_url and schema
        try:
            service_details = self._get_service_details(service_id)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Failed to get service details for service {service_id}: {e}")
            raise KiteError(f"Failed to get service details for service {service_id}: {e}")

        service_url = service_details.get("service_url")
        if not service_url:
            if self.verbose:
                self.logger.error(f"No service_url found for service {service_id}")
            raise KiteError(f"No service_url found for service {service_id}")

        # Validate payload against OpenAPI schema
        schema = service_details.get("schema")
        if schema:
            try:
                # Find matching endpoint and method
                path, method = find_matching_endpoint(service_url, schema)
                if path and method:
                    if self.verbose:
                        self.logger.debug(f"Validating payload against OpenAPI schema for {path} {method}")
                    # Validate payload against OpenAPI schema for the specific endpoint
                    validate_payload_against_openapi(payload, schema, path, method)
                else:
                    warning_msg = f"Warning: No matching endpoint found in schema for service URL: {service_url}"
                    if self.verbose:
                        self.logger.warning(warning_msg)
                    print(warning_msg)
            except Exception as e:
                warning_msg = f"Warning: Error processing OpenAPI schema: {e}"
                if self.verbose:
                    self.logger.warning(warning_msg)
                print(warning_msg)

        try:
            # Make request to service endpoint
            url = f'{self.base_url}/v1/service/{service_id}'
            request_body = {"data": payload}
            
            # Merge additional headers
            request_headers = dict(self.session.headers)
            request_headers.update(headers)
            
            self._log_http_request("POST", url, headers=request_headers, body=request_body)
            
            response = self.session.post(url, json=request_body, headers=headers)
            self._log_http_response(response)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Network error calling service {service_id}: {e}")
            raise KiteNetworkError(f"Failed to call service {service_id}: {e}")

        result = self._handle_service_response(response)
        if self.verbose:
            self.logger.debug(f"Service call result: {result}")
        return result

    def get_service_info(self, service_id: str) -> str:
        """
        Get a human-readable description of the service including endpoints and request/response format.

        Args:
            service_id: The service ID to get information for

        Returns:
            Human-readable description of the service
        """
        self._log_method_call("get_service_info", service_id=service_id)
        
        try:
            service_details = self._get_service_details(service_id)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Failed to get service details for service {service_id}: {e}")
            raise KiteError(f"Failed to get service details for service {service_id}: {e}")

        schema = service_details.get("schema")
        description = service_details.get("description", "No description available")

        # Build the human-readable description
        info_parts = []

        # Basic service info
        info_parts.append(f"Service ID: {service_id}")
        info_parts.append(f"Description: {description}")

        if schema:
            try:
                schema_description = openapi_to_description(schema)
                info_parts.append(schema_description)
                if self.verbose:
                    self.logger.debug(f"Generated schema description for {service_id}")
            except Exception as e:
                error_msg = f"Error parsing OpenAPI schema: {e}"
                if self.verbose:
                    self.logger.warning(error_msg)
                info_parts.append(error_msg)
        else:
            no_schema_msg = "\nNo OpenAPI schema available for this service"
            if self.verbose:
                self.logger.debug(no_schema_msg)
            info_parts.append(no_schema_msg)

        result = "\n".join(info_parts)
        if self.verbose:
            self.logger.debug(f"Service info result length: {len(result)} characters")
        return result

    def _handle_response(self, response):
        """Handle HTTP response uniformly"""
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise KiteError("Invalid response from server")

        if 200 <= response.status_code < 300:
            return data

        if response.status_code == 401 or response.status_code == 403:
            raise KiteAuthenticationError(
                f"Authentication failed (status {response.status_code}): {data.get('error', response.text)}"
            )
        elif response.status_code == 404:
            raise KiteNotFoundError(
                f"Resource not found (status {response.status_code}): {data.get('error', response.text)}"
            )
        elif 400 <= response.status_code < 500:
            raise KiteError(
                f"Client error (status {response.status_code}): {data.get('error', response.text)}"
            )
        elif 500 <= response.status_code < 600:
            raise KiteError(
                f"Server error (status {response.status_code}): {data.get('error', response.text)}"
            )
        else:
            error_msg = data.get("error", "Unknown error")
            raise KiteError(error_msg)

    def _handle_service_response(self, response: requests.Response) -> dict:
        """Handle service response uniformly"""
        if not 200 <= response.status_code < 300:
            raise KiteError(f"Service error (status {response.status_code}): {response.text}")

        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            print(f"Warning: cannot jsonify service response: {response.text}")
            return response.text
        except Exception as e:
            print(f"Warning: cannot jsonify service response: {response.text} {e}")
            return response.text
