"""
Shared models cho System Integrator Authentication
Được sử dụng bởi Auth Service, User Service và các service consumer
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from cores.model.base_model import CamelCaseModel, DataResponse


class SystemIntegratorType(Enum):
    """Loại System Integrator"""

    API_CLIENT = "API_CLIENT"
    SERVICE_TO_SERVICE = "SERVICE_TO_SERVICE"
    EXTERNAL_INTEGRATION = "EXTERNAL_INTEGRATION"


class TokenType(Enum):
    """Loại token trong hệ thống"""

    REGULAR_USER = "REGULAR_USER"
    SYSTEM_INTEGRATOR = "SYSTEM_INTEGRATOR"
    SERVICE_TO_SERVICE = "SERVICE_TO_SERVICE"


# === Request/Response Models ===


class ClientCredentialsRequest(BaseModel):
    """Request model cho Client Credentials Grant"""

    client_id: str = Field(
        ..., min_length=1, max_length=255, description="Client ID"
    )
    client_secret: str = Field(
        ..., min_length=1, max_length=255, description="Client Secret"
    )
    grant_type: str = Field(
        default="client_credentials", pattern="^client_credentials$"
    )
    scope: Optional[str] = Field(
        None, max_length=500, description="Requested scopes (space-separated)"
    )


class SystemIntegratorTokenResponse(CamelCaseModel):
    """Response model cho System Integrator token"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(
        ..., description="Token expiration time in seconds"
    )
    scope: Optional[str] = Field(None, description="Granted scopes")
    client_id: str = Field(..., description="Client ID")
    usage_instructions: Optional[dict] = Field(
        None, description="Usage instructions"
    )


class SystemIntegratorValidationRequest(BaseModel):
    """Request model cho token validation"""

    access_token: str = Field(..., description="Token to validate")
    target_service_id: str = Field(..., description="Target service ID")


class SystemIntegratorValidationResponse(CamelCaseModel):
    """Response model cho token validation"""

    valid: bool = Field(..., description="Token validity")
    user_token: Optional[str] = Field(
        None, description="Generated user token for the request"
    )
    client_info: Optional[dict] = Field(None, description="Client information")
    error_message: Optional[str] = Field(
        None, description="Error message if validation fails"
    )


class SystemIntegratorIntrospectResponse(CamelCaseModel):
    """Response model cho token introspection"""

    id: int = Field(..., description="System user ID")
    client_id: str = Field(..., description="Client ID")
    user_type: str = Field(default="SYSTEM", description="User type")
    is_system_integrator: bool = Field(
        default=True, description="Is system integrator flag"
    )
    scopes: List[str] = Field(default_factory=list, description="Token scopes")


class SystemIntegratorPermissionRequest(BaseModel):
    """Request model cho permission check"""

    route: str = Field(..., description="API route to check")
    method: str = Field(..., description="HTTP method")
    table_management_id: Optional[str] = Field(
        None, description="Table management ID"
    )


class SystemIntegratorPermissionResponse(CamelCaseModel):
    """Response model cho permission check"""

    can_action: bool = Field(..., description="Permission granted")
    user_id: int = Field(..., description="System user ID")
    client_id: str = Field(..., description="Client ID")
    permission_source: str = Field(
        default="SYSTEM_INTEGRATOR", description="Permission source"
    )
    reason: Optional[str] = Field(None, description="Reason if denied")


# === Domain Models ===


class SystemIntegratorClient(BaseModel):
    """Domain model cho System Integrator Client"""

    id: Optional[int] = None
    client_id: str
    client_secret_hash: str
    client_name: str
    description: Optional[str] = None
    client_type: SystemIntegratorType = SystemIntegratorType.API_CLIENT
    service_management_id: str
    jwt_secret: str
    allowed_scopes: List[str] = Field(default_factory=list)
    allowed_target_services: List[str] = Field(default_factory=list)
    is_active: bool = True
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None


class SystemIntegratorToken(BaseModel):
    """Domain model cho System Integrator token"""

    token_hash: str
    client_id: str
    scopes: List[str]
    expires_at: datetime
    is_revoked: bool = False
    created_at: Optional[datetime] = None


# === JWT Payload Models ===


class SystemIntegratorJWTPayload(BaseModel):
    """JWT Payload cho System Integrator token"""

    sub: str = "system_integrator"
    client_id: str
    client_type: SystemIntegratorType
    service_management_id: str
    scopes: List[str]
    token_type: TokenType = TokenType.SYSTEM_INTEGRATOR
    exp: datetime
    iat: datetime
    jti: Optional[str] = None  # JWT ID for revocation


class SystemUserTokenPayload(BaseModel):
    """JWT Payload cho System User token (user-token trong headers)"""

    id: int = -1  # Special system user ID
    client_id: str
    token_type: TokenType = TokenType.SYSTEM_INTEGRATOR
    exp: datetime
    iat: Optional[datetime] = None


# === Error Models ===


class SystemIntegratorError(Exception):
    """Base exception cho System Integrator"""

    def __init__(
        self, message: str, error_code: str = "SYSTEM_INTEGRATOR_ERROR"
    ):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class InvalidClientError(SystemIntegratorError):
    """Exception khi client credentials không hợp lệ"""

    def __init__(self, message: str = "Invalid client credentials"):
        super().__init__(message, "INVALID_CLIENT")


class TokenExpiredError(SystemIntegratorError):
    """Exception khi token đã hết hạn"""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, "TOKEN_EXPIRED")


class InsufficientScopeError(SystemIntegratorError):
    """Exception khi không đủ scope/permission"""

    def __init__(self, message: str = "Insufficient scope or permissions"):
        super().__init__(message, "INSUFFICIENT_SCOPE")


# === Response Wrappers ===


class SystemIntegratorTokenDataResponse(
    DataResponse[SystemIntegratorTokenResponse]
):
    """Wrapped response cho token endpoint"""


class SystemIntegratorValidationDataResponse(
    DataResponse[SystemIntegratorValidationResponse]
):
    """Wrapped response cho validation endpoint"""


class SystemIntegratorIntrospectDataResponse(
    DataResponse[SystemIntegratorIntrospectResponse]
):
    """Wrapped response cho introspect endpoint"""


class SystemIntegratorPermissionDataResponse(
    DataResponse[SystemIntegratorPermissionResponse]
):
    """Wrapped response cho permission check endpoint"""
