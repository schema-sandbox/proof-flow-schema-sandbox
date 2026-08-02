"""Authentication helpers and opt-in API-key/HMAC middleware.

The local Alpha.4 workflow stays unauthenticated when bound to loopback.  Production
must explicitly configure both ``PROOFFLOW_SECRET_KEY`` and ``PROOFFLOW_API_KEYS``.
The token format is intentionally a small signed envelope, not a JWT; callers should
not mistake it for an OAuth/OIDC implementation.
"""

from __future__ import annotations

import hmac
import json
import logging
import time
from base64 import b64decode, b64encode
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

_CURRENT_AUTH_USER: ContextVar["AuthUser | None"] = ContextVar(
    "proofflow_current_auth_user", default=None
)


@dataclass
class AuthUser:
    user_id: str
    roles: list[str]
    is_admin: bool = False


class AuthMiddleware:
    """
    Middleware for validating API Keys and HMAC-signed tokens.
    """

    def __init__(self, secret_key: str | None = None, valid_api_keys: list[str] | None = None) -> None:
        self.secret_key = secret_key.encode("utf-8") if secret_key else None
        self.valid_api_keys = {key for key in (valid_api_keys or []) if key}

    def validate_api_key(self, api_key: str) -> bool:
        """Validate API Key against allowed keys."""
        return any(hmac.compare_digest(api_key, candidate) for candidate in self.valid_api_keys)

    def create_token(
        self,
        user_id: str,
        roles: list[str] | None = None,
        ttl_seconds: int = 3600,
    ) -> str:
        """Create a short-lived HMAC-signed token."""
        if self.secret_key is None:
            raise ValueError("a secret key is required to create tokens")
        now = int(time.time())
        payload = json.dumps(
            {
                "user_id": user_id,
                "roles": roles or ["user"],
                "iat": now,
                "exp": now + max(ttl_seconds, 1),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        signature = hmac.new(self.secret_key, payload.encode("utf-8"), "sha256").hexdigest()
        b64_payload = b64encode(payload.encode("utf-8"), altchars=b"-_").decode("ascii")
        return f"{b64_payload}.{signature}"

    def verify_token(self, token: str) -> AuthUser | None:
        """Verify HMAC-signed token and return AuthUser or None."""
        try:
            if self.secret_key is None:
                return None
            b64_payload, signature = token.split(".", maxsplit=1)
            payload_bytes = b64decode(b64_payload.encode("ascii"), altchars=b"-_", validate=True)
            expected_sig = hmac.new(self.secret_key, payload_bytes, "sha256").hexdigest()

            if not hmac.compare_digest(signature, expected_sig):
                return None

            data = json.loads(payload_bytes.decode("utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("user_id"), str):
                return None
            roles = data.get("roles", [])
            if not isinstance(roles, list) or not all(isinstance(role, str) for role in roles):
                return None
            issued_at = data.get("iat")
            expires_at = data.get("exp")
            if not isinstance(issued_at, int) or not isinstance(expires_at, int):
                return None
            if expires_at <= int(time.time()):
                return None
            return AuthUser(
                user_id=data["user_id"],
                roles=roles,
                is_admin="admin" in roles,
            )
        except Exception:
            return None


def current_auth_user() -> AuthUser | None:
    """Return the authenticated principal for the current request, if any."""

    return _CURRENT_AUTH_USER.get()


def authenticated_actor(default: Any) -> Any:
    """Replace client-supplied audit identity when a request is authenticated."""

    user = current_auth_user()
    if user is None:
        return default
    from .domain import Actor, ActorType

    return Actor(type=ActorType.HUMAN, id=user.user_id, display_name=user.user_id)


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """Require an API key or short-lived HMAC token for ``/api/`` requests."""

    def __init__(self, app: Any, *, secret_key: str, valid_api_keys: tuple[str, ...]) -> None:
        if not secret_key or not valid_api_keys:
            raise ValueError("production authentication requires a secret and at least one API key")
        super().__init__(app)
        self.auth = AuthMiddleware(secret_key=secret_key, valid_api_keys=list(valid_api_keys))

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        if not request.url.path.startswith("/api/"):
            return await call_next(request)

        user: AuthUser | None = None
        api_key = request.headers.get("x-api-key")
        if api_key and self.auth.validate_api_key(api_key):
            user = AuthUser(user_id="api-key", roles=["api"])
        else:
            authorization = request.headers.get("authorization", "")
            if authorization.lower().startswith("bearer "):
                user = self.auth.verify_token(authorization[7:].strip())
        if user is None:
            return JSONResponse({"detail": "authentication required"}, status_code=401)

        token = _CURRENT_AUTH_USER.set(user)
        try:
            return await call_next(request)
        finally:
            _CURRENT_AUTH_USER.reset(token)
