import base64
import hashlib
import hmac
import ipaddress
import os
from typing import List, Optional

from cryptography.fernet import Fernet
from starlette.requests import Request

from appodus_utils.common.commons import Utils
from appodus_utils.exception.exceptions import ForbiddenException, UnauthorizedException

client_secret_encryption_key = os.getenv('APPODUS_CLIENT_SECRET_ENCRYPTION_KEY')
client_request_expires_seconds: int = int(os.getenv('APPODUS_CLIENT_REQUEST_EXPIRES_SECONDS', 300))
fernet = Fernet(client_secret_encryption_key)

class ClientUtils:

    @staticmethod
    def get_client_ip(request: Request) -> str:
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            # X-Forwarded-For may contain a list of IPs
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.client.host
        return ip

    @staticmethod
    def is_ip_allowed(ip: str, allowed_ips: List[str]) -> bool:
        try:
            client_ip = ipaddress.ip_address(ip)
            return any(client_ip == ipaddress.ip_address(allowed) for allowed in allowed_ips)
        except ValueError:
            return False

    @staticmethod
    def extract_domain_from_referer_or_origin(header: Optional[str]) -> Optional[str]:
        try:
            from urllib.parse import urlparse
            if header:
                parsed = urlparse(header)
                return parsed.hostname
        except Exception:
            pass
        return None

    @staticmethod
    def encrypt_api_secret(secret: bytes) -> str:
        return fernet.encrypt(secret).decode()

    @staticmethod
    def decrypt_api_secret(encrypted_secret: str) -> str:
        return fernet.decrypt(encrypted_secret.encode()).decode()

    @staticmethod
    def compute_signature(client_secret: str, method: str, path: str, timestamp: str, body: bytes) -> str:
        body_hash = hashlib.sha256(body).hexdigest()

        canonical_msg = f"{method}\n{path}\n{str(timestamp)}\n{body_hash}"

        expected_signature = hmac.new(
            key=client_secret.encode(),
            msg=canonical_msg.encode(),
            digestmod=hashlib.sha256
        ).digest()

        expected_signature_b64 = base64.b64encode(expected_signature).decode()

        return expected_signature_b64

    @staticmethod
    async def verify_signature(request: Request, client_secret: str):
        client_id = request.headers.get("x-client-id")
        signature = request.headers.get("x-signature")
        timestamp = request.headers.get("x-timestamp")

        if not client_secret:
            raise ForbiddenException(message="Invalid Client ID")

        if not all([client_id, signature, timestamp]):
            raise UnauthorizedException(message="Missing headers")

        if not Utils.timestamp_now_minus_less_than(client_request_expires_seconds, timestamp):
            raise UnauthorizedException(message="Request expired")

        body = await request.body()
        path = str(request.url.path)
        method = request.method.upper()
        client_secret_decrypted = ClientUtils.decrypt_api_secret(client_secret)

        expected_signature = ClientUtils.compute_signature(client_secret_decrypted, method, path, timestamp, body)

        if not hmac.compare_digest(expected_signature, signature):
            raise ForbiddenException(message="Invalid signature")
