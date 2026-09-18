from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import RequesterIdentity


class AdjudicationStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUIRES_MANUAL_REVIEW = "REQUIRES_MANUAL_REVIEW"

class ClaimRequest(BaseModel):
    claim_id: str = Field(..., min_length=1, description="Unique insurance claim reference identifier.")
    encounter_id: str = Field(..., min_length=1, description="Associated clinical encounter ID.")
    tpa_id: str = Field(..., min_length=1, description="Identifier of the reviewing insurance company.")
    package_code: str = Field(..., min_length=1, description="Official PM-JAY tariff code submitted for reimbursement.")
    claimed_amount_inr: float = Field(..., gt=0, description="Amount requested by the hospital in Indian Rupees.")
    fhir_bundle: Dict[str, Any] = Field(..., description="The generated FHIR bundle to be cross-examined.")

    requester: RequesterIdentity

    @field_validator("claimed_amount_inr")
    @classmethod
    def amount_must_be_reasonable(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("claimed_amount_inr must be a positive amount")
        return value

class ClaimResponse(BaseModel):
    adjudication_status: AdjudicationStatus
    approved_amount_inr: float
    pre_auth_token: Optional[str] = None
    adjudication_notes: str
