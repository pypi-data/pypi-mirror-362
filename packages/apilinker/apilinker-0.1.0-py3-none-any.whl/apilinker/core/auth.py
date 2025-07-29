"""
Authentication module for handling API authentication.
"""

import logging
import os
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AuthConfig(BaseModel):
    """Base authentication configuration."""
    
    type: str
    
    class Config:
        extra = "allow"


class ApiKeyAuth(AuthConfig):
    """API Key authentication configuration."""
    
    type: str = "api_key"
    key: str
    header_name: str = "X-API-Key"
    in_header: bool = True
    in_query: bool = False
    query_param: Optional[str] = None


class BearerAuth(AuthConfig):
    """Bearer token authentication configuration."""
    
    type: str = "bearer"
    token: str


class BasicAuth(AuthConfig):
    """Basic authentication configuration."""
    
    type: str = "basic"
    username: str
    password: str


class OAuth2ClientCredentials(AuthConfig):
    """OAuth2 client credentials authentication configuration."""
    
    type: str = "oauth2_client_credentials"
    client_id: str
    client_secret: str
    token_url: str
    scope: Optional[str] = None
    token: Optional[str] = None
    expires_at: Optional[int] = None


class AuthManager:
    """
    Manager for handling different types of authentication.
    
    This class creates and manages authentication configurations for different APIs.
    It supports API Key, Bearer Token, Basic Auth, and OAuth2 client credentials.
    """
    
    def __init__(self) -> None:
        logger.debug("Initialized AuthManager")
    
    def _resolve_env_vars(self, value: Any) -> Any:
        """
        Resolve environment variables in a string value.
        
        Args:
            value: Value that may contain environment variable references like ${VAR_NAME}
            
        Returns:
            Value with environment variables resolved
        """
        if not isinstance(value, str):
            return value
            
        if value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env_value = os.environ.get(env_var)
            if env_value is None:
                logger.warning(f"Environment variable {env_var} not found")
                return value
            return env_value
            
        return value
    
    def _resolve_env_vars_in_dict(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively resolve environment variables in a dictionary.
        
        Args:
            config: Dictionary that may contain environment variable references
            
        Returns:
            Dictionary with environment variables resolved
        """
        resolved: Dict[str, Any] = {}
        
        for key, value in config.items():
            if isinstance(value, dict):
                resolved[key] = self._resolve_env_vars_in_dict(value)
            elif isinstance(value, str):
                resolved[key] = self._resolve_env_vars(value)
            else:
                resolved[key] = value
                
        return resolved
    
    def configure_auth(self, auth_config: Dict[str, Any]) -> AuthConfig:
        """
        Configure authentication based on provided configuration.
        
        Args:
            auth_config: Authentication configuration dictionary
            
        Returns:
            AuthConfig instance for the specified authentication type
        """
        # Resolve any environment variables in the config
        auth_config = self._resolve_env_vars_in_dict(auth_config)
        
        auth_type = auth_config.get("type", "").lower()
        
        if auth_type == "api_key":
            if "key" not in auth_config:
                raise ValueError("API Key authentication requires 'key' parameter")
                
            # Determine if API key goes in header or query parameter
            in_header = True
            in_query = False
            header_name = auth_config.get("header", "X-API-Key")
            query_param = None
            
            if "in" in auth_config:
                location = str(auth_config["in"]).lower()
                if location == "query":
                    in_header = False
                    in_query = True
                    query_param = auth_config.get("param_name", "api_key")
                    
            return ApiKeyAuth(
                key=str(auth_config["key"]),
                header_name=header_name,
                in_header=in_header,
                in_query=in_query,
                query_param=query_param
            )
            
        elif auth_type == "bearer":
            if "token" not in auth_config:
                raise ValueError("Bearer authentication requires 'token' parameter")
                
            return BearerAuth(token=str(auth_config["token"]))
            
        elif auth_type == "basic":
            if "username" not in auth_config or "password" not in auth_config:
                raise ValueError("Basic authentication requires 'username' and 'password' parameters")
                
            return BasicAuth(
                username=str(auth_config["username"]),
                password=str(auth_config["password"])
            )
            
        elif auth_type in ["oauth2", "oauth2_client_credentials"]:
            required_params = ["client_id", "client_secret", "token_url"]
            missing_params = [param for param in required_params if param not in auth_config]
            
            if missing_params:
                raise ValueError(f"OAuth2 client credentials authentication requires {', '.join(missing_params)} parameters")
                
            return OAuth2ClientCredentials(
                client_id=auth_config["client_id"],
                client_secret=auth_config["client_secret"],
                token_url=auth_config["token_url"],
                scope=auth_config.get("scope"),
                token=auth_config.get("token"),
                expires_at=auth_config.get("expires_at")
            )
            
        else:
            logger.warning(f"Unknown authentication type: {auth_type}, using base AuthConfig")
            # Remove type from auth_config to avoid duplicate parameter error
            auth_config_copy = auth_config.copy()
            auth_config_copy.pop('type', None)
            return AuthConfig(type=auth_type, **auth_config_copy)
            
    def refresh_oauth2_token(self, auth_config: OAuth2ClientCredentials) -> OAuth2ClientCredentials:
        """
        Refresh an OAuth2 token using client credentials flow.
        
        Args:
            auth_config: OAuth2 client credentials configuration
            
        Returns:
            Updated OAuth2ClientCredentials with new token and expiry
        """
        try:
            import httpx
            import time
            from datetime import datetime, timedelta
            
            data = {
                "grant_type": "client_credentials",
                "client_id": auth_config.client_id,
                "client_secret": auth_config.client_secret,
            }
            
            if auth_config.scope:
                data["scope"] = auth_config.scope
            
            response = httpx.post(
                auth_config.token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            token_data = response.json()
            
            # Update token and expiry
            token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
            expires_at = int(time.time() + expires_in)
            
            logger.debug("OAuth2 token refreshed")
            
            return OAuth2ClientCredentials(
                type=auth_config.type,
                client_id=auth_config.client_id,
                client_secret=auth_config.client_secret,
                token_url=auth_config.token_url,
                scope=auth_config.scope,
                token=token,
                expires_at=expires_at
            )
            
        except Exception as e:
            logger.error(f"Error refreshing OAuth2 token: {str(e)}")
            raise
