"""
Configuration cho System Integrator
"""

import os


class SystemIntegratorConfig:
    """Configuration cho System Integrator features"""

    # JWT Configuration
    JWT_ALGORITHM = "HS256"
    DEFAULT_TOKEN_EXPIRY_HOURS = int(
        os.getenv("SI_DEFAULT_TOKEN_EXPIRY_HOURS", "24")
    )
    SYSTEM_USER_TOKEN_SECRET = os.getenv(
        "SI_SYSTEM_USER_TOKEN_SECRET",
        "system-integrator-user-token-secret-2024",
    )

    # Default Client Configuration
    DEFAULT_CLIENT_ID = os.getenv(
        "SI_DEFAULT_CLIENT_ID", "royalty-integrator-001"
    )
    DEFAULT_CLIENT_SECRET = os.getenv(
        "SI_DEFAULT_CLIENT_SECRET", "royalty-secret-2024"
    )

    # Service URLs
    AUTH_SERVICE_URL = os.getenv(
        "AUTH_SERVICE_URL", "http://auth-service:8100"
    )
    USER_SERVICE_URL = os.getenv(
        "USER_SERVICE_URL", "http://user-service:8001"
    )

    # Security Settings
    ENABLE_TOKEN_REVOCATION = (
        os.getenv("SI_ENABLE_TOKEN_REVOCATION", "false").lower() == "true"
    )
    MAX_TOKEN_PER_CLIENT = int(os.getenv("SI_MAX_TOKEN_PER_CLIENT", "10"))

    # Permission Settings
    DEFAULT_SCOPES = [
        "royalty:read",
        "royalty:write",
        "news:read",
        "user:read",
    ]

    # Endpoint Paths
    ENDPOINT_PATHS = {
        "AUTH_AUTHENTICATE": "system-integrator/authenticate",
        "AUTH_VALIDATE": "system-integrator/validate",
        "USER_INTROSPECT": "system-integrator/introspect",
        "USER_CHECK_PERMISSION": "system-integrator/check-permission",
    }

    @classmethod
    def get_endpoint_url(cls, service: str, endpoint: str) -> str:
        """Get full URL cho endpoint"""
        base_urls = {
            "auth": cls.AUTH_SERVICE_URL,
            "user": cls.USER_SERVICE_URL,
        }

        base_url = base_urls.get(service.lower())
        if not base_url:
            raise ValueError(f"Unknown service: {service}")

        endpoint_path = cls.ENDPOINT_PATHS.get(endpoint)
        if not endpoint_path:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        return f"{base_url.rstrip('/')}/{endpoint_path}"

    @classmethod
    def is_development_mode(cls) -> bool:
        """Check if running in development mode"""
        return os.getenv("APP_ENV", "local").lower() in [
            "local",
            "development",
            "dev",
        ]
