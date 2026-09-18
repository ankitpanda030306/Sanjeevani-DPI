from typing import Any, Dict, Optional


class GatewayError(Exception):
    """Base class for all handled application errors."""

    status_code: int = 500

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class InvalidRequestError(GatewayError):
    """400 - request is well-formed JSON but violates a business rule."""

    status_code = 400


class AuthorizationDeniedError(GatewayError):
    """403 - Cedar policy engine evaluated the request to DENY.

    Per the spec's default-deny invariant, this MUST be raised before any
    language model or claims logic is invoked.
    """

    status_code = 403


class UpstreamServiceError(GatewayError):
    """502 - a downstream dependency (Bedrock, Cedar) failed unexpectedly."""

    status_code = 502


class UpstreamTimeoutError(GatewayError):
    """504 - a downstream dependency (Bedrock, Cedar) did not respond in time."""

    status_code = 504
