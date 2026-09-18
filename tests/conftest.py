import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def valid_encounter_payload() -> dict:
    return {
        "encounter_id": "ENC-0001",
        "abha_id": "91-1234-5678-9012",
        "requester": {"user_id": "U-100", "role": "Doctor", "facility_id": "F-01"},
        "encounter_type": "OPD",
        "raw_narrative": "Patient presents with elevated fasting glucose and fatigue.",
        "s3_audio_url": None,
    }


@pytest.fixture
def valid_claim_payload() -> dict:
    return {
        "claim_id": "CLM-0001",
        "encounter_id": "ENC-0001",
        "tpa_id": "TPA-01",
        "package_code": "HBP-S-001",
        "claimed_amount_inr": 5000.0,
        "fhir_bundle": {"resourceType": "Bundle", "type": "collection", "entry": []},
        "requester": {"user_id": "U-200", "role": "InsuranceTPA", "facility_id": "F-01"},
    }
