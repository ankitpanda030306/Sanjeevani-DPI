import logging

from fastapi import APIRouter

from app.exceptions import AuthorizationDeniedError
from app.schemas.claim import ClaimRequest, ClaimResponse
from app.schemas.common import AccessDecision
from app.security.cedar_engine import check_authorization
from app.services.ai_pipeline import adjudicate_claim as run_claim_adjudication

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Insurance Claims"])


@router.post(
    "/adjudicate-claim",
    response_model=ClaimResponse,
    summary="Adjudicate Health Claim",
    description=(
        "Evaluates an Ayushman Bharat insurance claim against official "
        "National Health Authority benefit schedules and detects duplicate "
        "or unbundled billing items."
    ),
)
async def adjudicate_claim(payload: ClaimRequest) -> ClaimResponse:
    # Step 1: Confirm the insurance TPA is authorized to inspect claim
    # lines and issue pre-authorization. Default-deny applies.
    authorization = await check_authorization(
        requester=payload.requester,
        action="AdjudicateClaim",
        resource="ClaimRecord",
    )

    if authorization.decision == AccessDecision.DENY:
        logger.warning(
            "Claim adjudication denied by Cedar",
            extra={"context": {"claim_id": payload.claim_id, "reason": authorization.reason}},
        )
        raise AuthorizationDeniedError(
            message="Access denied by the Cedar Policy Engine.",
            details={"policy_id": authorization.policy_id, "reason": authorization.reason},
        )

    # Step 2: Delegate to the claims adjudication agent.
    result = await run_claim_adjudication(
        fhir_bundle=payload.fhir_bundle,
        package_code=payload.package_code,
        claimed_amount_inr=payload.claimed_amount_inr,
    )

    # Step 3: Return the verdict.
    return ClaimResponse(
        adjudication_status=result["adjudication_status"],
        approved_amount_inr=result["approved_amount_inr"],
        pre_auth_token=result["pre_auth_token"],
        adjudication_notes=result["adjudication_notes"],
    )
