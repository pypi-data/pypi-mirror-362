"""
Main ApiLinker class that orchestrates the connection, mapping, and data transfer between APIs.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel

from apilinker.core.auth import AuthManager
from apilinker.core.connector import ApiConnector
from apilinker.core.logger import setup_logger
from apilinker.core.mapper import FieldMapper
from apilinker.core.scheduler import Scheduler


class SyncResult(BaseModel):
    """Result of a sync operation."""
    
    count: int = 0
    success: bool = True
    errors: List[str] = []
    details: Dict[str, Any] = {}


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
             params: Optional[Dict[str, Any]] = None) -> SyncResult:
        """
        Execute a sync operation between source and target APIs.
        
        Args:
            source_endpoint: Source endpoint to use (overrides mapping)
            target_endpoint: Target endpoint to use (overrides mapping)
            params: Additional parameters for the source API call
            
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
        
        self.logger.info(f"Starting sync from {source_endpoint} to {target_endpoint}")
        
        try:
            # Fetch data from source
            source_data = self.source.fetch_data(source_endpoint, params)
            
            # Map fields according to configuration
            transformed_data = self.mapper.map_data(source_endpoint, target_endpoint, source_data)
            
            # Send data to target
            result = self.target.send_data(target_endpoint, transformed_data)
            
            # Create result object
            sync_result = SyncResult(
                count=len(transformed_data) if isinstance(transformed_data, list) else 1,
                success=True,
                details={"source_count": len(source_data) if isinstance(source_data, list) else 1}
            )
            
            self.logger.info(f"Sync completed successfully: {sync_result.count} items transferred")
            return sync_result
            
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            return SyncResult(
                count=0,
                success=False,
                errors=[str(e)]
            )
    
    def start_scheduled_sync(self) -> None:
        """Start scheduled sync operations."""
        self.logger.info("Starting scheduled sync")
        self.scheduler.start(self.sync)
    
    def stop_scheduled_sync(self) -> None:
        """Stop scheduled sync operations."""
        self.logger.info("Stopping scheduled sync")
        self.scheduler.stop()
