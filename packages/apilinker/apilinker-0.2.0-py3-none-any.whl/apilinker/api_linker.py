"""
Main ApiLinker class that orchestrates the connection, mapping, and data transfer between APIs.
"""

import logging
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel, Field

from apilinker.core.auth import AuthManager
from apilinker.core.connector import ApiConnector
from apilinker.core.logger import setup_logger
from apilinker.core.mapper import FieldMapper
from apilinker.core.scheduler import Scheduler


class ErrorDetail(BaseModel):
    """Detailed error information for API requests."""
    
    message: str
    status_code: Optional[int] = None
    response_body: Optional[str] = None
    request_url: Optional[str] = None
    request_method: Optional[str] = None
    timestamp: Optional[str] = None
    error_type: str = "general"


class SyncResult(BaseModel):
    """Result of a sync operation with enhanced error reporting."""
    
    count: int = 0
    success: bool = True
    errors: List[ErrorDetail] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_response: Dict[str, Any] = Field(default_factory=dict)
    target_response: Dict[str, Any] = Field(default_factory=dict)
    duration_ms: Optional[int] = None


class ApiLinker:
    """
    Main class for connecting, mapping and transferring data between APIs.
    
    This class orchestrates the entire process of:
    1. Connecting to source and target APIs
    2. Fetching data from the source
    3. Mapping fields according to configuration
    4. Transforming data as needed
    5. Sending data to the target
    6. Scheduling recurring operations
    
    Args:
        config_path: Path to YAML/JSON configuration file
        source_config: Direct source configuration dictionary
        target_config: Direct target configuration dictionary
        mapping_config: Direct mapping configuration dictionary
        schedule_config: Direct scheduling configuration dictionary
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        source_config: Optional[Dict[str, Any]] = None,
        target_config: Optional[Dict[str, Any]] = None,
        mapping_config: Optional[Dict[str, Any]] = None,
        schedule_config: Optional[Dict[str, Any]] = None,
        log_level: str = "INFO",
        log_file: Optional[str] = None,
    ) -> None:
        # Initialize logger
        self.logger = setup_logger(log_level, log_file)
        self.logger.info("Initializing ApiLinker")
        
        # Initialize components
        self.source: Optional[ApiConnector] = None
        self.target: Optional[ApiConnector] = None
        self.mapper = FieldMapper()
        self.scheduler = Scheduler()
        self.auth_manager = AuthManager()
        
        # Load configuration if provided
        if config_path:
            self.load_config(config_path)
        else:
            # Set up direct configurations if provided
            if source_config:
                self.add_source(**source_config)
            if target_config:
                self.add_target(**target_config)
            if mapping_config:
                self.add_mapping(**mapping_config)
            if schedule_config:
                self.add_schedule(**schedule_config)
    
    def load_config(self, config_path: str) -> None:
        """
        Load configuration from a YAML or JSON file.
        
        Args:
            config_path: Path to the configuration file
        """
        self.logger.info(f"Loading configuration from {config_path}")
        
        # Resolve environment variables in config path
        config_path = os.path.expandvars(config_path)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        # Set up components from config
        if "source" in config:
            self.add_source(**config["source"])
        
        if "target" in config:
            self.add_target(**config["target"])
        
        if "mapping" in config:
            if isinstance(config["mapping"], list):
                for mapping in config["mapping"]:
                    self.add_mapping(**mapping)
            else:
                self.add_mapping(**config["mapping"])
        
        if "schedule" in config:
            self.add_schedule(**config["schedule"])
        
        if "logging" in config:
            log_config = config["logging"]
            log_level = log_config.get("level", "INFO")
            log_file = log_config.get("file")
            self.logger = setup_logger(log_level, log_file)
    
    def add_source(self, type: str, base_url: str, auth: Optional[Dict[str, Any]] = None, 
                  endpoints: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        """
        Add a source API connector.
        
        Args:
            type: Type of API connector (rest, graphql, etc.)
            base_url: Base URL of the API
            auth: Authentication configuration
            endpoints: Configured endpoints
            **kwargs: Additional configuration parameters
        """
        self.logger.info(f"Adding source connector: {type} for {base_url}")
        
        # Set up authentication if provided
        if auth:
            auth_config = self.auth_manager.configure_auth(auth)
        else:
            auth_config = None
        
        # Create source connector
        self.source = ApiConnector(
            connector_type=type,
            base_url=base_url,
            auth_config=auth_config,
            endpoints=endpoints or {},
            **kwargs
        )
    
    def add_target(self, type: str, base_url: str, auth: Optional[Dict[str, Any]] = None,
                  endpoints: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        """
        Add a target API connector.
        
        Args:
            type: Type of API connector (rest, graphql, etc.)
            base_url: Base URL of the API
            auth: Authentication configuration
            endpoints: Configured endpoints
            **kwargs: Additional configuration parameters
        """
        self.logger.info(f"Adding target connector: {type} for {base_url}")
        
        # Set up authentication if provided
        if auth:
            auth_config = self.auth_manager.configure_auth(auth)
        else:
            auth_config = None
        
        # Create target connector
        self.target = ApiConnector(
            connector_type=type,
            base_url=base_url,
            auth_config=auth_config,
            endpoints=endpoints or {},
            **kwargs
        )
    
    def add_mapping(self, source: str, target: str, fields: List[Dict[str, Any]]) -> None:
        """
        Add a field mapping between source and target endpoints.
        
        Args:
            source: Source endpoint name
            target: Target endpoint name
            fields: List of field mappings
        """
        self.logger.info(f"Adding mapping from {source} to {target} with {len(fields)} fields")
        self.mapper.add_mapping(source, target, fields)
    
    def add_schedule(self, type: str, **kwargs: Any) -> None:
        """
        Add a schedule for recurring syncs.
        
        Args:
            type: Type of schedule (interval, cron)
            **kwargs: Schedule-specific parameters
        """
        self.logger.info(f"Adding schedule: {type}")
        self.scheduler.add_schedule(type, **kwargs)
    
    def sync(self, source_endpoint: Optional[str] = None, 
             target_endpoint: Optional[str] = None,
             params: Optional[Dict[str, Any]] = None,
             max_retries: int = 3,
             retry_delay: float = 1.0,
             retry_backoff_factor: float = 2.0,
             retry_status_codes: Optional[List[int]] = None) -> SyncResult:
        """
        Execute a sync operation between source and target APIs.
        
        Args:
            source_endpoint: Source endpoint to use (overrides mapping)
            target_endpoint: Target endpoint to use (overrides mapping)
            params: Additional parameters for the source API call
            max_retries: Maximum number of retry attempts for transient failures
            retry_delay: Initial delay between retries in seconds
            retry_backoff_factor: Multiplicative factor for retry delay
            retry_status_codes: HTTP status codes to retry (default: 429, 502, 503, 504)
            
        Returns:
            SyncResult: Result of the sync operation
        """
        if not self.source or not self.target:
            raise ValueError("Source and target connectors must be configured before syncing")
        
        # If no endpoints specified, use the first mapping
        if not source_endpoint or not target_endpoint:
            mapping = self.mapper.get_first_mapping()
            if not mapping:
                raise ValueError("No mapping configured and no endpoints specified")
            source_endpoint = mapping["source"]
            target_endpoint = mapping["target"]
        
        # Generate correlation ID for this sync operation
        correlation_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Default retry status codes if none provided
        if retry_status_codes is None:
            retry_status_codes = [429, 502, 503, 504]  # Common transient failures
            
        self.logger.info(f"[{correlation_id}] Starting sync from {source_endpoint} to {target_endpoint}")
        
        # Initialize result object
        sync_result = SyncResult(correlation_id=correlation_id)
        
        # Fetch data from source with retries
        source_data, source_error = self._with_retries(
            operation=lambda: self.source.fetch_data(source_endpoint, params),
            operation_name=f"fetch from {source_endpoint}",
            max_retries=max_retries,
            retry_delay=retry_delay,
            retry_backoff_factor=retry_backoff_factor,
            retry_status_codes=retry_status_codes,
            correlation_id=correlation_id
        )
        
        if source_error:
            end_time = time.time()
            sync_result.duration_ms = int((end_time - start_time) * 1000)
            sync_result.success = False
            sync_result.errors.append(source_error)
            self.logger.error(f"[{correlation_id}] Sync failed: {source_error.message}")
            return sync_result
            
        try:
            # Map fields according to configuration
            transformed_data = self.mapper.map_data(source_endpoint, target_endpoint, source_data)
            
            # Record source data metrics
            source_count = len(source_data) if isinstance(source_data, list) else 1
            sync_result.details["source_count"] = source_count
            
            # Send data to target with retries
            target_result, target_error = self._with_retries(
                operation=lambda: self.target.send_data(target_endpoint, transformed_data),
                operation_name=f"send to {target_endpoint}",
                max_retries=max_retries,
                retry_delay=retry_delay,
                retry_backoff_factor=retry_backoff_factor,
                retry_status_codes=retry_status_codes,
                correlation_id=correlation_id
            )
            
            if target_error:
                end_time = time.time()
                sync_result.duration_ms = int((end_time - start_time) * 1000)
                sync_result.success = False
                sync_result.errors.append(target_error)
                self.logger.error(f"[{correlation_id}] Sync failed: {target_error.message}")
                return sync_result
                
            # Update result with success information
            sync_result.count = len(transformed_data) if isinstance(transformed_data, list) else 1
            sync_result.success = True
            sync_result.target_response = target_result if isinstance(target_result, dict) else {}
            
            # Calculate duration
            end_time = time.time()
            sync_result.duration_ms = int((end_time - start_time) * 1000)
            
            self.logger.info(
                f"[{correlation_id}] Sync completed successfully: {sync_result.count} items transferred in {sync_result.duration_ms}ms"
            )
            return sync_result
            
        except Exception as e:
            end_time = time.time()
            error_detail = ErrorDetail(
                message=str(e),
                error_type="mapping_error",
                timestamp=datetime.now().isoformat()
            )
            
            self.logger.error(f"[{correlation_id}] Sync failed during mapping: {str(e)}")
            
            sync_result.duration_ms = int((end_time - start_time) * 1000)
            sync_result.success = False
            sync_result.errors.append(error_detail)
            
            return sync_result
    
    def start_scheduled_sync(self) -> None:
        """Start scheduled sync operations."""
        self.logger.info("Starting scheduled sync")
        self.scheduler.start(self.sync)
    
    def stop_scheduled_sync(self) -> None:
        """Stop scheduled sync operations."""
        self.logger.info("Stopping scheduled sync")
        self.scheduler.stop()
        
    def _with_retries(self, operation: Callable[[], Any], operation_name: str,
                     max_retries: int, retry_delay: float, retry_backoff_factor: float,
                     retry_status_codes: List[int], correlation_id: str) -> Tuple[Any, Optional[ErrorDetail]]:
        """
        Execute an operation with configurable retry logic for transient failures.
        
        Args:
            operation: Callable function to execute
            operation_name: Name of operation for logging
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
            retry_backoff_factor: Multiplicative factor for retry delay
            retry_status_codes: HTTP status codes that should trigger a retry
            correlation_id: Correlation ID for tracing
            
        Returns:
            Tuple of (result, error_detail) - If successful, error_detail will be None
        """
        current_delay = retry_delay
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    self.logger.info(
                        f"[{correlation_id}] Retry attempt {attempt}/{max_retries} for {operation_name} after {current_delay:.2f}s delay"
                    )
                    time.sleep(current_delay)
                    current_delay *= retry_backoff_factor
                
                result = operation()
                
                if attempt > 0:
                    self.logger.info(f"[{correlation_id}] Retry succeeded for {operation_name}")
                    
                return result, None
                
            except Exception as e:
                last_exception = e
                status_code = getattr(e, 'status_code', None)
                response_body = getattr(e, 'response', None)
                request_url = getattr(e, 'url', None)
                request_method = getattr(e, 'method', None)
                
                # Convert response to string if it's not already
                if response_body and not isinstance(response_body, str):
                    try:
                        response_body = str(response_body)[:1000]  # Limit size
                    except:
                        response_body = "<Unable to convert response to string>"
                
                error_detail = ErrorDetail(
                    message=str(e),
                    status_code=status_code,
                    response_body=response_body,
                    request_url=request_url,
                    request_method=request_method,
                    timestamp=datetime.now().isoformat(),
                    error_type="transient_error" if status_code in retry_status_codes else "api_error"
                )
                
                # Check if this is a retryable error
                is_retryable = status_code in retry_status_codes if status_code else False
                
                if is_retryable and attempt < max_retries:
                    self.logger.warning(
                        f"[{correlation_id}] {operation_name} failed with retryable error (status: {status_code}): {str(e)}"
                    )
                else:
                    # Either not retryable or out of retries
                    log_level = logging.WARNING if is_retryable else logging.ERROR
                    retry_msg = "out of retry attempts" if is_retryable else "non-retryable error"
                    
                    self.logger.log(
                        log_level,
                        f"[{correlation_id}] {operation_name} failed with {retry_msg}: {str(e)}"
                    )
                    return None, error_detail
        
        # We should never reach here, but just in case
        fallback_error = ErrorDetail(
            message=f"Unknown error during {operation_name}",
            timestamp=datetime.now().isoformat(),
            error_type="unknown_error"
        )
        return None, fallback_error
