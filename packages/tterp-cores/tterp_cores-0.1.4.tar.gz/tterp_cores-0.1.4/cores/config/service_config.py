"""
Service configuration module - Cấu hình cho các microservices khác
"""

import os
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load các biến môi trường từ file .env
load_dotenv()


class AccessToken(BaseSettings):
    """Cấu hình cho access token"""

    USER_SECRET_KEY: str | None = None
    EXPIRES_IN: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class ServiceConfig(BaseSettings):
    """Cấu hình các service tương tác lẫn nhau"""

    # Service URLs
    BASE_URL: str = "http://proxy:8000/"
    AUTH_BASE_URL: str = "http://auth_service:8000/"
    PROFILE_BASE_URL: str = "http://profile_service:8000/"
    USER_BASE_URL: str = "http://user_service:8000/"
    VOTE_BASE_URL: str = "http://vote_service:8000/"
    MANAGEMENT_BASE_URL: str = "http://management_service:8016/"
    NOTIFIER_BASE_URL: str = "http://notifier:8000/"
    COLLABORATOR_BASE_URL: str = "http://collaborator:8000/"
    BOOKING_BASE_URL: str = "http://booking_service:8000/"
    AUTHENTICATOR_BASE_URL: str = "http://192.168.61.40:8022/"
    SSO_BASE_URL: str = ""

    # Service IDs
    BASE_SERVICE_ID: str = ""
    AUTH_SERVICE_ID: str = "auth-service"
    PROFILE_SERVICE_ID: str = "profile-service"
    USER_SERVICE_ID: str = "user-service"
    VOTE_SERVICE_ID: str = "competition-vote-service"
    NOTIFIER_SERVICE_ID: str = "notifier-service"
    RESOURCE_SERVICE_ID: str = "resource-service"
    SSO_SERVICE_ID: str = "sso-service"
    COLLABORATOR_SERVICE_ID: str = "collaborator-service"
    BOOKING_SERVICE_ID: str = "booking-service"

    # Các endpoint paths
    ENDPOINT_PATHS: Dict[str, str] = {
        "AUTH_AUTHENTICATE": "system-integrator/authenticate",
        "AUTH_VALIDATE": "system-integrator/validate",
        "USER_INTROSPECT": "system-integrator/introspect",
        "USER_CHECK_PERMISSION": "system-integrator/check-permission",
    }

    # Secret keys
    AUTH_SECRET_KEY: str = ""
    SECRET_KEY_FOR_MANAGEMENT: str = ""

    # URLs
    FE_BASE_URL: str = ""
    FE_VERIFY_PEN_NAME_URL: str = ""
    PROJECT_ROOT: str = ""

    # Cấu hình access token
    access_token: AccessToken = AccessToken()

    # Các cài đặt bổ sung
    ADMIN_MAIL: Optional[str] = None
    ENCRYPTION_KEY: Optional[str] = None
    USER_SECRET_KEY: Optional[str] = None
    API_SYNC_KEY: str = "sdfghuisfodhg"
    HOOK_API_KEY: str = "sdfghuisfodhg"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    def get_endpoint_url(self, service: str, endpoint: str) -> str:
        """Get full URL cho endpoint"""
        base_urls = {
            "auth": self.AUTH_BASE_URL,
            "user": self.USER_BASE_URL,
            "profile": self.PROFILE_BASE_URL,
            "notifier": self.NOTIFIER_BASE_URL,
        }

        base_url = base_urls.get(service.lower())
        if not base_url:
            raise ValueError(f"Unknown service: {service}")

        endpoint_path = self.ENDPOINT_PATHS.get(endpoint)
        if not endpoint_path:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        return f"{base_url.rstrip('/')}/{endpoint_path}"

    def is_development_mode(self) -> bool:
        """Check if running in development mode"""
        return os.getenv("APP_ENV", "local").lower() in [
            "local",
            "development",
            "dev",
        ]


# Singleton instance
service_config = ServiceConfig()
