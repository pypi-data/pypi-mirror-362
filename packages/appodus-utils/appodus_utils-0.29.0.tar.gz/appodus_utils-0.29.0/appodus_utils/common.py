import base64
import enum
import hashlib
import hmac
import ipaddress
import json
import os
import random
import re
import time
import uuid
from _decimal import Decimal
from datetime import datetime, timedelta, timezone
from typing import List, Union, Any, Dict, Optional, Literal

import inflection
from cryptography.fernet import Fernet
from fastapi import APIRouter, Path, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from jinja2 import Template
from jose import jwt
from passlib.context import CryptContext
from starlette.requests import Request

from appodus_utils.exception.exceptions import ForbiddenException, UnauthorizedException, AppodusBaseException

# Constants
CHUNK_SIZE = 64 * 1024  # 64 KB for streaming
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024


class Utils:
    default_max_miles_per_day = 200 * 365
    default_max_allowed_miles = 200 * 365
    pwd_context = CryptContext(schemes=["sha256_crypt"])

    # Datetime
    @staticmethod
    def datetime_now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def datetime_to_db(date: datetime) -> datetime:
        return date.replace(tzinfo=None)

    @staticmethod
    def datetime_now_to_db() -> datetime:
        return Utils.datetime_to_db(Utils.datetime_now())

    @staticmethod
    def datetime_from_db(date: datetime) -> datetime:
        return date.replace(tzinfo=timezone.utc)

    @staticmethod
    def datetime_now_plus(*, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0) -> datetime:
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        return Utils.datetime_now() + delta

    @staticmethod
    def get_time_diff_sec(start_datetime: datetime):
        if not datetime:
            return 0
        return (Utils.datetime_now() - start_datetime).total_seconds()

    @staticmethod
    def datetime_now_plus_less_than(plus_seconds: int, less_than_datetime: Union[str, datetime]) -> bool:
        if not less_than_datetime:
            return False
        if isinstance(less_than_datetime, str):
            less_than_datetime = datetime.fromisoformat(less_than_datetime)

        if not less_than_datetime.tzinfo:
            less_than_datetime = less_than_datetime.replace(tzinfo=timezone.utc)

        return Utils.datetime_now_plus(seconds=plus_seconds) < less_than_datetime

    @staticmethod
    def template_bind_context(content: str, context: Dict[str, Any]) -> str:
        template = Template(content)
        return template.render(context)

    @staticmethod
    def replace_em_dash(text: str) -> str:
        return re.sub(r'\s*—\s*', ' - ', text)

    @staticmethod
    def create_jwt(
            user_id: str,
            roles: Optional[List[str]],
            expires_in_sec: int,
            jwt_secret: str,
            jwt_algorithm: str
    ):
        payload = {
            "sub": user_id,
            "roles": roles,
            "exp": Utils.datetime_now() + timedelta(seconds=expires_in_sec),
            "iat": Utils.datetime_now()
        }
        return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)

    @staticmethod
    def set_secure_cookie(response: Response, key: str, value: str):
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,  # HTTPS only
            samesite="strict",
            max_age=3600,  # 1 hour
            path="/",
        )

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Utils.pwd_context.verify(secret=plain_password, hash=hashed_password)

    @staticmethod
    def sha256(value: str) -> str:
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    @staticmethod
    def md5(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    @staticmethod
    def get_password_hash(password: str) -> str:
        return Utils.pwd_context.hash(secret=password)

    @staticmethod
    def get_otp_code(prefix: str = None, suffix: str = None):
        otp = random.randint(100000, 999999)
        if prefix:
            otp = prefix + '-' + str(otp)
        if suffix:
            otp = otp + suffix

        return otp

    @staticmethod
    def get_tran_ref():
        now = Utils.datetime_now()
        uuid_str = uuid.uuid4().__str__()
        return f'{now.year}' \
               f'-{now.month}' \
               f'-{now.day}' \
               f'-{now.hour}' \
               f'_{now.minute}' \
               f'-{uuid_str[:6]}'

    @staticmethod
    def random_str(length: int = 6):
        if length > 36:
            raise AppodusBaseException(message=f"random_str: the maximum length is 36, you requested '{length}'")
        uuid_str = uuid.uuid4().__str__()
        return uuid_str[:length]

    @staticmethod
    def get_document_ref():
        return uuid.uuid1().hex

    @staticmethod
    def get_url_str(request: Request) -> str:
        components = request.url.components
        url = f'{components.scheme}s://{components.netloc}{components.path}?{components.query}'

        return url

    @classmethod
    def validate_checksum(cls, checksum: str, checksum_disabled: bool, **kwargs):
        if not checksum_disabled:
            scrambled_value = cls._get_checksum_scrambled_params(**kwargs)
            checksum_is_valid = cls.pwd_context.verify(scrambled_value, checksum)

            if not checksum_is_valid:
                raise ValueError("Process cannot proceed, invalid checksum.")

    @classmethod
    def generate_checksum(cls, checksum_disabled: bool, **kwargs):
        if not checksum_disabled:
            scrambled_value = cls._get_checksum_scrambled_params(**kwargs)
            return Utils.pwd_context.hash(scrambled_value)

        return "checksum"

    @staticmethod
    def _get_checksum_scrambled_params(**kwargs):
        input_value = ''
        for key, value in kwargs.items():
            value = jsonable_encoder(value)
            if isinstance(value, dict):
                value = json.dumps(value)
            input_value += value
        scrambled_value = ''
        special_chars = '%$'
        for i in reversed(input_value):
            scrambled_value += i + special_chars

        return scrambled_value

    @staticmethod
    def hex_to_uuid(value: str):
        return uuid.UUID(hex=value, version=4) if isinstance(value, str) else value

    @staticmethod
    def uuid_to_hex(value: uuid.UUID):
        return value.hex if value and isinstance(value, uuid.UUID) else value

    @staticmethod
    def convert_camel_to_snake_case(field: str):
        return inflection.underscore(field)

    @staticmethod
    def convert_snake_to_camel_case(field: str):
        return inflection.camelize(field, False)

    @staticmethod
    def obj_convert_field_set_value(in_obj: Union[dict, Any], camel_cased: bool = True, raise_exception: bool = False):
        supplementary_dict = {}

        if not in_obj or isinstance(in_obj, str):
            return in_obj

        if not isinstance(in_obj, dict):
            in_obj = in_obj.model_dump()

        in_obj_copy = in_obj.copy()
        for field in in_obj:
            if camel_cased:
                converted_field = Utils.convert_snake_to_camel_case(field)
            else:
                converted_field = Utils.convert_camel_to_snake_case(field)

            if converted_field:
                try:

                    if isinstance(in_obj[field], dict):
                        converted_dic = Utils.obj_convert_field_set_value(in_obj[field], camel_cased, raise_exception)
                        supplementary_dict.setdefault(converted_field, converted_dic)
                    elif isinstance(in_obj[field], list):
                        for obj in in_obj[field]:

                            if isinstance(obj, datetime):
                                converted_list = '{:%Y-%m-%dT%H:%M:%S}'.format(obj)
                            elif isinstance(obj, enum.Enum):
                                converted_list = obj.name
                            elif not isinstance(obj, list) and not isinstance(obj, dict):
                                converted_list = obj
                            else:
                                converted_list = Utils.obj_convert_field_set_value(obj, camel_cased, raise_exception)

                            existing_values: list = supplementary_dict.get(converted_field)
                            if existing_values:
                                existing_values.append(converted_list)
                            else:
                                existing_values = [converted_list]
                            supplementary_dict.setdefault(converted_field, existing_values)
                    elif isinstance(in_obj[field], datetime):
                        converted = '{:%Y-%m-%dT%H:%M:%S}'.format(in_obj[field])
                        supplementary_dict.setdefault(converted_field, converted)
                    elif isinstance(in_obj[field], Decimal):
                        converted = str(in_obj[field])
                        supplementary_dict.setdefault(converted_field, converted)
                    elif isinstance(in_obj[field], enum.Enum):
                        converted = in_obj[field].name
                        supplementary_dict.setdefault(converted_field, converted)
                    else:
                        supplementary_dict.setdefault(converted_field, in_obj[field])
                    in_obj_copy.pop(field)
                except AttributeError as e:
                    # TODO logger.error
                    if raise_exception:
                        raise e

        supplementary_dict.update(in_obj_copy)
        return supplementary_dict

    @staticmethod
    def remove_dash(value: str) -> str:
        return value.replace('-', '')

    @staticmethod
    def advanced_bold_formatting(text: str, style: Literal['math', 'sans', 'double'] = 'math'):
        """
        Handles multiple bold segments with regex for better edge case handling
        Supports: *bold*, **bold**, __bold__, or custom delimiters
        """
        # Define character mappings (truncated for example)
        bold_map = {
            'math': {
                'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡',
                'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩',
                'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱',
                'y': '𝐲', 'z': '𝐳',
                'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇',
                'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏',
                'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗',
                'Y': '𝐘', 'Z': '𝐙',
                '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕',
                '8': '𝟖', '9': '𝟗'
            },
            'sans': {
                'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵',
                'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽',
                'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅',
                'y': '𝘆', 'z': '𝘇',
                'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛',
                'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
                'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫',
                'Y': '𝗬', 'Z': '𝗭',
                '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳',
                '8': '𝟴', '9': '𝟵'
            },
            'double': {
                'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙',
                'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡',
                'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩',
                'y': '𝕪', 'z': '𝕫',
                'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾', 'H': 'ℍ',
                'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆', 'P': 'ℙ',
                'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏',
                'Y': '𝕐', 'Z': 'ℤ',
                '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜', '5': '𝟝', '6': '𝟞', '7': '𝟟',
                '8': '𝟠', '9': '𝟡'
            }
        }.get(style)

        def bold_replacer(match):
            return ''.join([bold_map.get(c, c) for c in match.group(1)])

        # Process both **text** and __text__ patterns
        text = re.sub(r'\*(.*?)\*', bold_replacer, text)  # *text*
        text = re.sub(r'\*\*(.*?)\*\*', bold_replacer, text)  # **text**
        text = re.sub(r'__(.*?)__', bold_replacer, text)  # __text__

        return text

    @staticmethod
    def validate_file_size(file_path: Path, max_size: int) -> None:
        """
        Validate that a file does not exceed the allowed maximum size.

        Args:
            file_path (Path): Path to the file to validate.
            max_size (int):


        Raises:
            AttachmentError: If the file size exceeds max_size.
        """

        file_size = file_path.stat().st_size
        if file_size > max_size:
            raise ValueError(
                f"File {file_path.name} is too large ({file_size // (1024 * 1024)}MB). Max allowed size is {MAX_ATTACHMENT_SIZE // (1024 * 1024)}MB"
            )

client_secret_encryption_key = os.getenv('CLIENT_SECRET_ENCRYPTION_KEY')
client_request_expires_seconds: int = int(os.getenv('CLIENT_REQUEST_EXPIRES_SECONDS', 300))
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
    def compute_signature(secret, method, path, timestamp, body):
        msg = method + path + str(timestamp) + body
        return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    async def verify_signature(request: Request, client_secret: str):
        client_id = request.headers.get("x-client-id")
        signature = request.headers.get("x-signature")
        timestamp = request.headers.get("x-timestamp")

        if not client_secret:
            raise ForbiddenException(message="Invalid Client ID")

        if not all([client_id, signature, timestamp]):
            raise UnauthorizedException(message="Missing headers")

        if abs(int(time.time()) - int(timestamp)) > client_request_expires_seconds:
            raise UnauthorizedException(message="Request expired")

        body = await request.body()
        path = str(request.url.path)
        method = request.method.upper()

        expected_signature = ClientUtils.compute_signature(client_secret, method, path, timestamp, body.decode())

        if not hmac.compare_digest(expected_signature, signature):
            raise ForbiddenException(message="Invalid signature")

class RouterUtils:

    @classmethod
    def add_routers(cls, parent_router: APIRouter, children_routers: List[APIRouter]):
        for childrenRouter in children_routers:
            parent_router.include_router(childrenRouter)
            cls._remove_tagged_child_routes(parent_router, childrenRouter)

    @classmethod
    def _remove_tagged_child_routes(cls, parent_router: APIRouter, child_router: APIRouter):
        for route in parent_router.routes:
            if route.name in [r.name for r in child_router.routes]:
                for tag in parent_router.tags:
                    if tag in route.tags:
                        route.tags.remove(tag)

class FileUtils:

    @staticmethod
    async def get_file_size(file: UploadFile) -> int:
        """
        Determines the total size of the uploaded file in bytes.

        Args:
            file (UploadFile): The file to check.

        Returns:
            int: File size in bytes.
        """
        file.file.seek(0, 2)  # Seek to end
        size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        return size

class Base64Utils:
    @staticmethod
    def str_to_base64(input_str: str):
        input_bytes = input_str.encode('ascii')
        base64_bytes = base64.b64encode(input_bytes)
        base64_output = base64_bytes.decode('ascii')

        return base64_output

    @staticmethod
    def base64_to_str(input_base64):
        base64_bytes = input_base64.encode('ascii')
        string_bytes = base64.b64decode(base64_bytes)
        output_str = string_bytes.decode('ascii')

        return output_str

    @staticmethod
    def file_path_to_base64(file_path: Path) -> str:
        """
        Stream a file and encode it into Base64 to minimize memory usage.

        Args:
            file_path (Path): Path to the file to encode.

        Returns:
            str: Base64-encoded string of the file contents.
        """
        b64_encoded = bytearray()

        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                b64_chunk = base64.b64encode(chunk)
                b64_encoded.extend(b64_chunk)

        return b64_encoded.decode('utf-8')

    @staticmethod
    def read_base64_part(input_str: str):
        if input_str:
            split_value = input_str.split(';base64,')
            if len(split_value) > 1:
                return split_value[1]

            return input_str

        return None
