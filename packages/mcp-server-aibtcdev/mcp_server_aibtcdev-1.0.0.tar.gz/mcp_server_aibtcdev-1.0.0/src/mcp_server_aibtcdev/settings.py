"""
Configuration and settings for the aibtcdev MCP server.

This module handles environment variable configuration and provides
a centralized configuration class for API settings.
"""

import os
from typing import Dict


class APIConfig:
    """Configuration for API endpoints and authentication"""

    def __init__(self):
        self.base_url = os.getenv("AIBTC_API_BASE_URL", "https://api.aibtc.dev")
        self.bearer_token = os.getenv("AIBTC_BEARER_TOKEN")
        self.api_key = os.getenv("AIBTC_API_KEY")

        # Validate that at least one authentication method is available
        if not self.bearer_token and not self.api_key:
            print(
                "⚠️  Warning: No authentication credentials found in environment variables."
            )
            print(
                "   Set AIBTC_BEARER_TOKEN or AIBTC_API_KEY to authenticate API requests."
            )

    def has_auth(self) -> bool:
        """Check if authentication credentials are available"""
        return bool(self.bearer_token or self.api_key)

    def get_auth_headers(self, auth_type: str = "auto") -> Dict[str, str]:
        """Get authentication headers based on available credentials"""
        headers = {"Content-Type": "application/json"}

        if auth_type == "bearer" and self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        elif auth_type == "api_key" and self.api_key:
            headers["X-API-Key"] = self.api_key
        elif auth_type == "auto":
            if self.bearer_token:
                headers["Authorization"] = f"Bearer {self.bearer_token}"
            elif self.api_key:
                headers["X-API-Key"] = self.api_key

        return headers


# Global configuration instance
config = APIConfig()
