def test_missing_required_field_returns_422(client, valid_encounter_payload):
    payload = valid_encounter_payload.copy()
    del payload["raw_narrative"]

    response = client.post("/process-encounter", json=payload)

    assert response.status_code == 422


def test_invalid_encounter_type_returns_422(client, valid_encounter_payload):
    payload = valid_encounter_payload.copy()
    payload["encounter_type"] = "URGENT_CARE"  # not in the OPD | EMERGENCY enum

    response = client.post("/process-encounter", json=payload)

    assert response.status_code == 422


def test_whitespace_only_narrative_returns_422(client, valid_encounter_payload):
    payload = valid_encounter_payload.copy()
    payload["raw_narrative"] = "   "

    response = client.post("/process-encounter", json=payload)

    # Pydantic validators raise inside model validation -> FastAPI reports 422
    assert response.status_code == 422


def test_negative_claimed_amount_returns_422(client, valid_claim_payload):
    payload = valid_claim_payload.copy()
    payload["claimed_amount_inr"] = -100

    response = client.post("/adjudicate-claim", json=payload)

    assert response.status_code == 422


def test_health_check_returns_200(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["app_running"] is True
