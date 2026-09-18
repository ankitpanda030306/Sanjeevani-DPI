import logging

from fastapi import APIRouter

from app.exceptions import AuthorizationDeniedError
from app.schemas.common import AccessDecision, ExecutionStatus
from app.schemas.encounter import EncounterRequest, EncounterResponse
from app.security.cedar_engine import check_authorization
from app.services.ai_pipeline import execute_clinical_triage

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Clinical Encounters"])


@router.post(
    "/process-encounter",
    response_model=EncounterResponse,
    summary="Process Clinical Encounter",
    description=(
        "Ingests raw doctor notes or encounter audio references, validates "
        "medical provider access, coordinates clinical triage via AI agents, "
        "and outputs standardized diagnostic codes and ABDM FHIR schemas."
    ),
)
async def process_encounter(payload: EncounterRequest) -> EncounterResponse:
    # Step 1: Authorization -- MUST happen before any business logic runs.
    authorization = await check_authorization(
        requester=payload.requester,
        action="ExecuteTriage",
        resource="PatientRecord",
    )

    if authorization.decision == AccessDecision.DENY:
        logger.warning(
            "Encounter request denied by Cedar",
            extra={"context": {"encounter_id": payload.encounter_id, "reason": authorization.reason}},
        )
        raise AuthorizationDeniedError(
            message="Access denied by the Cedar Policy Engine.",
            details={"policy_id": authorization.policy_id, "reason": authorization.reason},
        )

    # Step 2: Delegate to the Strands multi-agent triage & coding pipeline.
    triage_result = await execute_clinical_triage(
        raw_narrative=payload.raw_narrative,
        encounter_type=payload.encounter_type.value,
        s3_audio_url=payload.s3_audio_url,
    )

    # Step 3: Return the consolidated payload.
    return EncounterResponse(
        status=ExecutionStatus.SUCCESS,
        access_decision=authorization.decision,
        diagnoses=triage_result["diagnoses"],
        suggested_package_code=triage_result["suggested_package_code"],
        fhir_bundle=triage_result["fhir_bundle"],
    )
