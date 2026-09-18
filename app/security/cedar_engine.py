"""
Integration point for ML/AI Developer 2's Cedar Policy Engine.

MOCK IMPLEMENTATION (Milestone 1)
----------------------------------
This module currently returns static, deterministic decisions so the Java
Spring Boot team can integrate against a stable contract immediately,
per Milestone 1 ("Expose dummy mock endpoints returning static data").

MILESTONE 2 INTEGRATION NOTE
----------------------------
When Developer 2 delivers the real Cedar Engine, replace the body of
`check_authorization` below with a call into their module, e.g.:

    from cedar_engine.policy import evaluate  # Developer 2's real package

    async def check_authorization(requester, action, resource, context=None):
        try:
            decision = await asyncio.wait_for(
                evaluate(principal=requester.model_dump(), action=action, resource=resource, context=context),
                timeout=settings.cedar_timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            raise UpstreamTimeoutError("Cedar policy engine timed out") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"Cedar policy engine failed: {exc}") from exc
        return AuthorizationResult(**decision)

Keep the function signature and return type identical so `routers/*.py`
never needs to change when the real engine is swapped in.
"""
import logging

from app.schemas.common import AccessDecision, AuthorizationResult, RequesterIdentity

logger = logging.getLogger(__name__)

_DENIED_ROLE_ACTION_PAIRS = {
    ("InsuranceTPA", "ExecuteTriage"), 
}


def _is_cedar_engine_loaded() -> bool:
    """Used by the /health endpoint. Always True for the mock."""
    return True


async def check_authorization(
    requester: RequesterIdentity,
    action: str,
    resource: str,
    context: dict | None = None,
) -> AuthorizationResult:
    """
    Evaluate whether `requester` may perform `action` on `resource`.

    Enforces default-deny: any role/action combination not explicitly
    allowed below is denied. Real Cedar policy files will replace this
    placeholder logic without changing the function signature.
    """
    logger.info(
        "Evaluating authorization",
        extra={
            "context": {
                "user_id": requester.user_id,
                "role": requester.role,
                "action": action,
                "resource": resource,
            }
        },
    )

    if (requester.role, action) in _DENIED_ROLE_ACTION_PAIRS:
        return AuthorizationResult(
            decision=AccessDecision.DENY,
            policy_id="mock-policy-role-restriction",
            reason=f"Role '{requester.role}' is not permitted to perform '{action}' on '{resource}'.",
        )

    # Default-deny invariant: only explicitly recognized roles are allowed.
    allowed_roles = {"Doctor", "Nurse", "InsuranceTPA", "Admin"}
    if requester.role not in allowed_roles:
        return AuthorizationResult(
            decision=AccessDecision.DENY,
            policy_id="mock-policy-default-deny",
            reason=f"Unrecognized role '{requester.role}'; default-deny applied.",
        )

    return AuthorizationResult(
        decision=AccessDecision.ALLOW,
        policy_id="mock-policy-allow-all-recognized-roles",
        reason=f"Role '{requester.role}' is permitted to perform '{action}' on '{resource}'.",
    )
