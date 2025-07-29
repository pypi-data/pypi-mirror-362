"""
API Connector module for handling connections to different types of APIs.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel, Field

from apilinker.core.auth import AuthConfig

logger = logging.getLogger(__name__)


class EndpointConfig(BaseModel):
    """Configuration for an API endpoint."""
    
    path: str
    method: str = "GET"
    params: Dict[str, Any] = Field(default_factory=dict)
    headers: Dict[str, str] = Field(default_factory=dict)
    body_template: Optional[Dict[str, Any]] = None
    pagination: Optional[Dict[str, Any]] = None
    response_path: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class ApiConnector:
    """
    API Connector for interacting with REST APIs.
    
    This class handles the connection to APIs, making requests, and
    processing responses.
    
    Args:
        connector_type: Type of connector (rest, graphql, etc.)
        base_url: Base URL for the API
        auth_config: Authentication configuration
        endpoints: Dictionary of endpoint configurations
        timeout: Request timeout in seconds
        retry_count: Number of retries on failure
        retry_delay: Delay between retries in seconds
    """
    
    def __init__(
        self,
        connector_type: str,
        base_url: str,
        auth_config: Optional[AuthConfig] = None,
        endpoints: Optional[Dict[str, Dict[str, Any]]] = None,
        timeout: int = 30,
        retry_count: int = 3,
        retry_delay: int = 1,
        **kwargs: Any,
    ) -> None:
        self.connector_type = connector_type
        self.base_url = base_url
        self.auth_config = auth_config
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
        # Parse and store endpoint configurations
        self.endpoints: Dict[str, EndpointConfig] = {}
        if endpoints:
            for name, config in endpoints.items():
                self.endpoints[name] = EndpointConfig(**config)
        
        # Store additional settings
        self.settings: Dict[str, Any] = kwargs
        
        # Create HTTP client with default settings
        self.client = self._create_client()
        
        logger.debug(f"Initialized {connector_type} connector for {base_url}")
    
    def _create_client(self) -> httpx.Client:
        """Create an HTTP client with appropriate settings."""
        # Initialize with default parameters
        auth = None
        if self.auth_config and self.auth_config.type == "basic" and hasattr(self.auth_config, "username") and hasattr(self.auth_config, "password"):
            auth = httpx.BasicAuth(
                username=getattr(self.auth_config, "username", ""),
                password=getattr(self.auth_config, "password", "")
            )
        
        # Create client with properly structured parameters
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            auth=auth
        )
    
    def _prepare_request(
        self, endpoint_name: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare a request for the given endpoint.
        
        Args:
            endpoint_name: Name of the endpoint to use
            params: Additional parameters to include in the request
            
        Returns:
            Dict containing request details (url, method, headers, params, json)
        """
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration")
        
        endpoint = self.endpoints[endpoint_name]
        
        # Combine endpoint path with base URL
        url = endpoint.path
        
        # Combine params from endpoint config and provided params
        request_params = endpoint.params.copy()
        if params:
            request_params.update(params)
        
        # Prepare headers
        headers = endpoint.headers.copy()
        
        # Add auth headers if needed
        if self.auth_config:
            if self.auth_config.type == "api_key" and hasattr(self.auth_config, "in_header") and getattr(self.auth_config, "in_header", False):
                header_name = getattr(self.auth_config, "header_name", "X-API-Key")
                key = getattr(self.auth_config, "key", "")
                headers[header_name] = key
            elif self.auth_config.type == "bearer" and hasattr(self.auth_config, "token"):
                headers["Authorization"] = f"Bearer {getattr(self.auth_config, 'token', '')}"
        
        # Prepare request object
        request = {
            "url": url,
            "method": endpoint.method,
            "headers": headers,
            "params": request_params,
        }
        
        # Add body if endpoint has a body template
        if endpoint.body_template:
            request["json"] = endpoint.body_template
        
        return request
    
    def _process_response(
        self, response: httpx.Response, endpoint_name: str
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Process the API response.
        
        Args:
            response: The HTTP response
            endpoint_name: Name of the endpoint
            
        Returns:
            Parsed response data
        """
        # Raise for HTTP errors
        response.raise_for_status()
        
        # Parse JSON response
        data: Union[Dict[str, Any], List[Dict[str, Any]]] = response.json()
        
        # Extract data from response path if configured
        endpoint = self.endpoints[endpoint_name]
        if endpoint.response_path and isinstance(data, dict):
            path_parts = endpoint.response_path.split(".")
            current_data: Any = data
            for part in path_parts:
                if isinstance(current_data, dict) and part in current_data:
                    current_data = current_data[part]
                else:
                    logger.warning(f"Response path '{endpoint.response_path}' not found in response")
                    break
            # Only update data if we successfully navigated through the path
            if current_data is not data:
                data = current_data
        
        # Ensure we return a valid type
        if isinstance(data, (dict, list)):
            return data
        else:
            # If response isn't a dict or list, wrap it in a dict
            return {"value": data}
    
    def _handle_pagination(
        self, initial_data: Union[Dict[str, Any], List[Dict[str, Any]]],
        endpoint_name: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Handle paginated responses if pagination is configured.
        
        Args:
            initial_data: Data from the first request
            endpoint_name: Name of the endpoint
            params: Request parameters
            
        Returns:
            Combined data from all pages
        """
        endpoint = self.endpoints[endpoint_name]
        
        # If no pagination config or initial data is not a dict, return as is
        if not endpoint.pagination or not isinstance(initial_data, dict):
            if isinstance(initial_data, list):
                return initial_data
            # Convert non-list data to a single-item list
            return [initial_data] if isinstance(initial_data, dict) else [{"value": initial_data}]
        
        # Extract the pagination configuration
        pagination = endpoint.pagination
        data_path = pagination.get("data_path", "")
        next_page_path = pagination.get("next_page_path", "")
        page_param = pagination.get("page_param", "page")
        
        # Extract the items from the first response
        if data_path:
            path_parts = data_path.split(".")
            items: Any = initial_data
            for part in path_parts:
                if isinstance(items, dict) and part in items:
                    items = items[part]
                else:
                    logger.warning(f"Data path '{data_path}' not found in response")
                    return [initial_data]
        else:
            # If no data path is specified, the entire response is the data
            items = initial_data
        
        # If items is not a list, make it a list
        if not isinstance(items, list):
            items = [items] if isinstance(items, dict) else [{"value": items}]
        
        # Extract next page token/URL if available
        next_page: Optional[Union[str, int]] = None
        if next_page_path:
            path_parts = next_page_path.split(".")
            temp_next_page: Any = initial_data
            for part in path_parts:
                if isinstance(temp_next_page, dict) and part in temp_next_page:
                    temp_next_page = temp_next_page[part]
                else:
                    temp_next_page = None
                    break
            # Only assign if it's a valid type for pagination
            if isinstance(temp_next_page, (str, int)):
                next_page = temp_next_page
        
        # Return the items if there's no next page
        if not next_page:
            return items
        
        # Fetch all pages
        all_items = items
        page = 2
        
        while next_page:
            # Update params for next page
            next_params: Dict[str, Any] = params.copy() if params else {}
            
            # Use either page number or next page token
            if isinstance(next_page, (str, int)):
                next_params[page_param] = next_page
            else:
                # If next_page is not a simple value, just increment page number
                next_params[page_param] = page
            
            # Make the next request
            try:
                request = self._prepare_request(endpoint_name, next_params)
                response = self.client.request(
                    request["method"],
                    request["url"],
                    headers=request["headers"],
                    params=request["params"],
                    json=request.get("json"),
                )
                response.raise_for_status()
                page_data = response.json()
                
                # Extract items from this page
                page_items: Any
                if data_path:
                    path_parts = data_path.split(".")
                    page_items = page_data
                    for part in path_parts:
                        if isinstance(page_items, dict) and part in page_items:
                            page_items = page_items[part]
                        else:
                            page_items = []
                            break
                else:
                    page_items = page_data
                
                # Add items to the result
                if isinstance(page_items, list):
                    all_items.extend(page_items)
                else:
                    all_items.append(page_items if isinstance(page_items, dict) else {"value": page_items})
                
                # Extract next page token
                if next_page_path:
                    path_parts = next_page_path.split(".")
                    temp_next_page = page_data
                    for part in path_parts:
                        if isinstance(temp_next_page, dict) and part in temp_next_page:
                            temp_next_page = temp_next_page[part]
                        else:
                            temp_next_page = None
                            break
                    # Only assign if it's a valid type for pagination
                    if isinstance(temp_next_page, (str, int)):
                        next_page = temp_next_page
                    else:
                        next_page = None
                else:
                    # If no next page path, just increment the page number
                    page += 1
                    next_page = page if page <= pagination.get("max_pages", 10) else None
                
            except Exception as e:
                logger.error(f"Error fetching page {page}: {str(e)}")
                break
        
        return all_items
    
    def fetch_data(
        self, endpoint_name: str, params: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Fetch data from the specified endpoint.
        
        Args:
            endpoint_name: Name of the endpoint to use
            params: Additional parameters for the request
            
        Returns:
            The parsed response data
        """
        logger.info(f"Fetching data from endpoint: {endpoint_name}")
        
        # Prepare the request
        request = self._prepare_request(endpoint_name, params)
        
        # Make the request with retries
        for attempt in range(1, self.retry_count + 1):
            try:
                logger.debug(f"Request attempt {attempt}: {request['method']} {request['url']}")
                
                response = self.client.request(
                    request["method"],
                    request["url"],
                    headers=request["headers"],
                    params=request["params"],
                    json=request.get("json"),
                )
                
                # Process the response
                data = self._process_response(response, endpoint_name)
                
                # Handle pagination if configured
                endpoint = self.endpoints[endpoint_name]
                if endpoint.pagination:
                    data = self._handle_pagination(data, endpoint_name, params)
                
                return data
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {str(e)}")
                if attempt < self.retry_count:
                    wait_time = self.retry_delay * attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
                    
            except Exception as e:
                logger.error(f"Error fetching data: {str(e)}")
                if attempt < self.retry_count:
                    wait_time = self.retry_delay * attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
    
    def send_data(
        self, endpoint_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Send data to the specified endpoint.
        
        Args:
            endpoint_name: Name of the endpoint to use
            data: Data to send
            
        Returns:
            The parsed response
        """
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration")
        
        endpoint = self.endpoints[endpoint_name]
        logger.info(f"Sending data to endpoint: {endpoint_name} ({endpoint.method} {endpoint.path})")
        
        # Prepare the request
        request = self._prepare_request(endpoint_name)
        
        # If data is a list, send each item individually
        if isinstance(data, list):
            results = []
            successful = 0
            failed = 0
            
            for item in data:
                try:
                    response = self.client.request(
                        request["method"],
                        request["url"],
                        headers=request["headers"],
                        params=request["params"],
                        json=item,
                    )
                    response.raise_for_status()
                    result = response.json() if response.content else {}
                    results.append(result)
                    successful += 1
                    
                except Exception as e:
                    logger.error(f"Error sending data item: {str(e)}")
                    failed += 1
            
            logger.info(f"Sent {successful} items successfully, {failed} failed")
            return {
                "success": True,
                "sent_count": successful,
                "failed_count": failed,
                "results": results,
            }
        
        # If data is a single item, send it
        else:
            # Make the request with retries
            for attempt in range(1, self.retry_count + 1):
                try:
                    response = self.client.request(
                        request["method"],
                        request["url"],
                        headers=request["headers"],
                        params=request["params"],
                        json=data,
                    )
                    response.raise_for_status()
                    result = response.json() if response.content else {}
                    
                    logger.info(f"Data sent successfully to {endpoint_name}")
                    return {
                        "success": True,
                        "result": result,
                    }
                    
                except Exception as e:
                    logger.error(f"Error sending data: {str(e)}")
                    if attempt < self.retry_count:
                        wait_time = self.retry_delay * attempt
                        logger.info(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise
            
            # This should not be reached due to the exception being raised in the loop
            return {"success": False, "error": "Unknown error"}
