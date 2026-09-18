# Sanjeevani-DPI AI Gateway (FastAPI)

AI Gateway and Policy Enforcement Layer that bridges the Java Spring Boot
backend with the Cedar Policy Engine and the Strands multi-agent AI system
on Amazon Bedrock. Implements the spec's 3 endpoints, default-deny
authorization, and standardized error handling.

## Project structure

```
app/
├── main.py                # FastAPI app, CORS, middleware, exception handlers, router wiring
├── config.py               # Environment-driven settings (Pydantic Settings)
├── logging_config.py       # Structured JSON logging
├── exceptions.py           # GatewayError hierarchy -> HTTP status codes
├── schemas/
│   ├── common.py           # RequesterIdentity, AccessDecision, ExecutionStatus
│   ├── encounter.py        # /process-encounter request & response contracts
│   ├── claim.py             # /adjudicate-claim request & response contracts
│   └── health.py            # /health response contract
├── security/
│   └── cedar_engine.py      # check_authorization() -- MOCK, replace in Milestone 2
├── services/
│   └── ai_pipeline.py       # execute_clinical_triage() & adjudicate_claim() -- MOCK, replace in Milestone 3
└── routers/
    ├── encounter.py         # POST /process-encounter
    ├── claim.py               # POST /adjudicate-claim
    └── health.py              # GET /health
tests/
├── conftest.py               # Shared fixtures (TestClient, sample payloads)
├── test_authorization.py     # Verifies default-deny -> 403 (Milestone 2 requirement)
└── test_validation.py        # Verifies 422 on malformed input, 200 on health
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

## Test

```bash
pytest tests/ -v
```

## Current state: Milestone 1 (mocked)

`app/security/cedar_engine.py` and `app/services/ai_pipeline.py` currently
return static/deterministic mock data so the Java team can integrate against
a stable contract immediately. Both modules document exactly how to wire in
the real implementations:

- **Milestone 2** — Developer 2 delivers the real Cedar Engine. Replace the
  body of `check_authorization()` in `cedar_engine.py`, keeping its
  signature (`requester, action, resource, context`) and its
  `AuthorizationResult` return type unchanged so the routers never need to
  change.
- **Milestone 3** — Developer 1 delivers the real Strands agents
  (Bedrock/Claude 3.5 Sonnet). Replace the bodies of
  `execute_clinical_triage()` and `adjudicate_claim()` in `ai_pipeline.py`
  the same way.

Both mock modules already show the target `asyncio.wait_for(...)` pattern
for turning Bedrock/Cedar timeouts and failures into the spec's `504`/`502`
responses via `UpstreamTimeoutError` / `UpstreamServiceError`
(`app/exceptions.py`).

## Design notes / assumptions

- **`/adjudicate-claim` requires a `requester` object.** The spec's table for
  this endpoint doesn't list one, but the workflow text says Cedar must
  "confirm the insurance TPA is authorized" — that check needs a principal
  to evaluate. A `RequesterIdentity` field (same shape as `/process-encounter`)
  was added to the request contract. Flag this to the Java team before
  Milestone 2 integration so their request payload matches.
- **Default-deny** is enforced in two places: any role not in the
  recognized set (`Doctor`, `Nurse`, `InsuranceTPA`, `Admin`) is denied, and
  specific role/action combinations (e.g. `InsuranceTPA` → `ExecuteTriage`)
  are explicitly denied even for recognized roles.
- **Error response shape** is consistent across all failure modes:
  `{"status": "FAILED", "error": "...", "details": {...}}`, so Java's
  client-side error handling can be written once.
- **`X-Request-ID`** is attached to every response and logged alongside
  method/path/status/duration for traceability in CloudWatch/ELK — useful
  given this service sits in a clinical + insurance compliance path.
