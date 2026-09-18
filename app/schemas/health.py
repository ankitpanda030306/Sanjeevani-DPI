from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_running: bool
    cedar_policies_loaded: bool
    bedrock_credentials_active: bool
