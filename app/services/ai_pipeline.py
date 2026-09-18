"""
Integration point for ML/AI Developer 1's Strands Multi-Agent System
(Claude 3.5 Sonnet on Amazon Bedrock).

MOCK IMPLEMENTATION (Milestone 1)
----------------------------------
Returns static, structurally-correct payloads so Java can integrate
immediately. Swap the bodies of `execute_clinical_triage` and
`adjudicate_claim` for real Bedrock/Strands calls in Milestone 3, keeping
the function signatures identical.

MILESTONE 3 INTEGRATION NOTE
----------------------------
Wrap the real Bedrock invocation similarly to:

    import asyncio
    import boto3
    from botocore.exceptions import ClientError, ReadTimeoutError

    async def execute_clinical_triage(raw_narrative, encounter_type, s3_audio_url=None):
        try:
            result = await asyncio.wait_for(
                strands_agent.run_triage(raw_narrative, encounter_type, s3_audio_url),
                timeout=settings.bedrock_timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            raise UpstreamTimeoutError("Bedrock triage agent timed out") from exc
        except (ClientError, ReadTimeoutError) as exc:
            raise UpstreamServiceError(f"Bedrock invocation failed: {exc}") from exc
        return result
"""
import logging
from typing import Any, Dict, List, Optional

from app.schemas.claim import AdjudicationStatus

logger = logging.getLogger(__name__)


def _is_bedrock_credentials_active() -> bool:
    """Used by the /health endpoint. Always True for the mock."""
    return True


async def execute_clinical_triage(
    raw_narrative: str,
    encounter_type: str,
    s3_audio_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract clinical entities, resolve ICD-10/SNOMED codes, and construct
    an ABDM FHIR bundle from a clinical narrative.

    Returns a dict shaped like:
        {
            "diagnoses": [Diagnosis, ...],
            "suggested_package_code": str,
            "fhir_bundle": dict,
        }
    """
    logger.info(
        "Running mock clinical triage",
        extra={"context": {"encounter_type": encounter_type, "narrative_length": len(raw_narrative)}},
    )

    diagnoses: List[Dict[str, str]] = [
        {
            "clinical_concept": "Type 2 Diabetes Mellitus",
            "icd10_code": "E11.9",
            "snomed_id": "44054006",
            "display": "Type 2 diabetes mellitus without complications",
        }
    ]

    fhir_bundle: Dict[str, Any] = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "Composition",
                    "status": "final",
                    "type": {"text": "OP Consult Note"},
                    "encounter": {"reference": "mock-encounter"},
                }
            }
        ],
    }

    return {
        "diagnoses": diagnoses,
        "suggested_package_code": "HBP-S-001" if encounter_type == "OPD" else "HBP-E-014",
        "fhir_bundle": fhir_bundle,
    }


async def adjudicate_claim(
    fhir_bundle: Dict[str, Any],
    package_code: str,
    claimed_amount_inr: float,
) -> Dict[str, Any]:
    """
    Evaluate a claim's FHIR bundle and claimed amount against NHA benefit
    schedules, and detect duplicate/unbundled billing items.

    Returns a dict shaped like:
        {
            "adjudication_status": AdjudicationStatus,
            "approved_amount_inr": float,
            "pre_auth_token": str | None,
            "adjudication_notes": str,
        }
    """
    logger.info(
        "Running mock claims adjudication",
        extra={"context": {"package_code": package_code, "claimed_amount_inr": claimed_amount_inr}},
    )
    mock_benefit_ceiling_inr = 15000.00

    if claimed_amount_inr <= mock_benefit_ceiling_inr:
        return {
            "adjudication_status": AdjudicationStatus.APPROVED,
            "approved_amount_inr": claimed_amount_inr,
            "pre_auth_token": "MOCK-PREAUTH-TOKEN-0001",
            "adjudication_notes": f"Claim within benefit schedule ceiling of INR {mock_benefit_ceiling_inr:.2f} for package '{package_code}'.",
        }

    return {
        "adjudication_status": AdjudicationStatus.REQUIRES_MANUAL_REVIEW,
        "approved_amount_inr": 0.0,
        "pre_auth_token": None,
        "adjudication_notes": (
            f"Claimed amount INR {claimed_amount_inr:.2f} exceeds the mock benefit schedule "
            f"ceiling of INR {mock_benefit_ceiling_inr:.2f} for package '{package_code}'. Flagged for manual review."
        ),
    }
