from enum import Enum

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class AccessDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class RequesterIdentity(BaseModel):
    """Identity of the human/system making the request, forwarded by Java."""

    user_id: str = Field(..., min_length=1, description="Unique identifier of the requesting user.")
    role: str = Field(..., min_length=1, description='Role of the requester, e.g. "Doctor", "InsuranceTPA".')
    facility_id: str = Field(..., min_length=1, description="Identifier of the healthcare facility.")


class AuthorizationResult(BaseModel):
    """Internal representation of a Cedar policy evaluation outcome."""

    decision: AccessDecision
    policy_id: str | None = None
    reason: str
