from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.security.cedar_engine import _is_cedar_engine_loaded
from app.services.ai_pipeline import _is_bedrock_credentials_active

router = APIRouter(tags=["System"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System health & readiness",
    description=(
        "Verifies the FastAPI application is running, local Cedar policy "
        "definitions are loaded into memory, and credentials for Amazon "
        "Bedrock invocation are active."
    ),
)
async def health_check() -> HealthResponse:
    cedar_ok = _is_cedar_engine_loaded()
    bedrock_ok = _is_bedrock_credentials_active()

    return HealthResponse(
        status="OK" if (cedar_ok and bedrock_ok) else "DEGRADED",
        app_running=True,
        cedar_policies_loaded=cedar_ok,
        bedrock_credentials_active=bedrock_ok,
    )
