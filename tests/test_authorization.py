"""
Milestone 2 requirement: "Write unit tests verifying that unauthorized
requests return HTTP 403."
"""


def test_process_encounter_denies_tpa_role(client, valid_encounter_payload):
    """InsuranceTPA is explicitly denied ExecuteTriage in the mock policy set."""
    payload = valid_encounter_payload.copy()
    payload["requester"] = {"user_id": "U-999", "role": "InsuranceTPA", "facility_id": "F-01"}

    response = client.post("/process-encounter", json=payload)

    assert response.status_code == 403
    body = response.json()
    assert body["status"] == "FAILED"
    assert "error" in body


def test_process_encounter_denies_unrecognized_role(client, valid_encounter_payload):
    """Default-deny invariant: unrecognized roles must never fall through to ALLOW."""
    payload = valid_encounter_payload.copy()
    payload["requester"] = {"user_id": "U-999", "role": "NotARealRole", "facility_id": "F-01"}

    response = client.post("/process-encounter", json=payload)

    assert response.status_code == 403


def test_process_encounter_allows_doctor(client, valid_encounter_payload):
    response = client.post("/process-encounter", json=valid_encounter_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "SUCCESS"
    assert body["access_decision"] == "ALLOW"
    assert "diagnoses" in body
    assert "fhir_bundle" in body


def test_adjudicate_claim_allows_tpa(client, valid_claim_payload):
    response = client.post("/adjudicate-claim", json=valid_claim_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["adjudication_status"] in {"APPROVED", "REJECTED", "REQUIRES_MANUAL_REVIEW"}


def test_adjudicate_claim_denies_unrecognized_role(client, valid_claim_payload):
    payload = valid_claim_payload.copy()
    payload["requester"] = {"user_id": "U-999", "role": "RandomRole", "facility_id": "F-01"}

    response = client.post("/adjudicate-claim", json=payload)

    assert response.status_code == 403
