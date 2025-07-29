import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from planar.logging import get_logger
from planar.security.auth_context import Principal, clear_principal, set_principal

logger = get_logger(__name__)

BASE_JWKS_URL = "https://auth-api.coplane.com/sso/jwks"
EXPECTED_ISSUER = "https://auth-api.coplane.com"


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        client_id: str,
        org_id: str | None = None,
        additional_exclusion_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.client_id = client_id
        self.org_id = org_id
        self.additional_exclusion_paths = additional_exclusion_paths or []

    def get_signing_key_from_jwt(self, client_id: str, token: str):
        jwks_url = f"{BASE_JWKS_URL}/{client_id}"
        jwks_client = jwt.PyJWKClient(jwks_url, cache_keys=True)
        return jwks_client.get_signing_key_from_jwt(token)

    def validate_jwt_token(self, token: str):
        signing_key = self.get_signing_key_from_jwt(self.client_id, token)

        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            issuer=EXPECTED_ISSUER,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
            },
        )

        org_id_from_token = payload.get("org_id")
        if self.org_id and org_id_from_token != self.org_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid organization",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    async def dispatch(self, request: Request, call_next):
        if (
            request.url.path
            in [
                "/docs",
                "/redoc",
                "/openapi.json",
                "/planar/v1/health",
            ]
            or request.url.path in self.additional_exclusion_paths
        ):
            return await call_next(request)

        principal_token = None
        try:
            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication scheme"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = authorization.replace("Bearer ", "")
            payload = self.validate_jwt_token(token)

            # Store payload in request state for backward compatibility
            request.state.user = payload

            # Create and set the principal in context
            principal = Principal.from_jwt_payload(payload)
            principal_token = set_principal(principal)

        except ValueError:
            # Handle invalid JWT payload structure
            logger.exception("invalid jwt payload structure")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid JWT payload structure"},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException as e:
            raise e
        except Exception:
            logger.exception("error validating jwt token")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authentication credentials"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            response = await call_next(request)
        finally:
            # Clean up the principal context
            if principal_token is not None:
                clear_principal(principal_token)

        return response
