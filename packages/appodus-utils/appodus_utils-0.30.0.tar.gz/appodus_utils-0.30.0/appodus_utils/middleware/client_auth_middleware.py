from appodus_utils.common import ClientUtils
from appodus_utils.domain.client.models import ClientRuleDto
from appodus_utils.domain.client.service import ClientService
from appodus_utils.exception.exceptions import ForbiddenException
from kink import di
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

client_service: ClientService = di[ClientService]

class ClientAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_id = request.headers.get("x-client-id")
        if not client_id or client_id not in await client_service.client_exists(client_id):
            return ForbiddenException(message="Missing or invalid API key")

        access_rules: ClientRuleDto = await client_service.get_client_access_rules(client_id)

        # --- IP Check ---
        client_ip = ClientUtils.get_client_ip(request)
        if not ClientUtils.is_ip_allowed(client_ip, access_rules.allowed_ips):
            return ForbiddenException(message=f"IP {client_ip} not allowed")

        # --- Origin / Referer Check ---
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        origin_domain = ClientUtils.extract_domain_from_referer_or_origin(origin) or ClientUtils.extract_domain_from_referer_or_origin(referer)

        if origin:
            if origin not in access_rules.allowed_origins:
                return ForbiddenException(message=f"Origin {origin} not allowed")
        elif referer:
            if origin_domain not in access_rules.allowed_domain:
                return ForbiddenException(message=f"Domain {origin_domain} not allowed")

        client_secret = await client_service.get_client_secret(client_id)
        await ClientUtils.verify_signature(request, client_secret)

        # --- Proceed with request ---
        response: Response = await call_next(request)

        # CORS headers (if Origin present and valid)
        if origin and origin in access_rules.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type,x-client-id"
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response
