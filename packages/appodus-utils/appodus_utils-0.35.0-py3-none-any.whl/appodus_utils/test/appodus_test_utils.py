import tempfile
from io import BytesIO
from typing import Type, List

from fastapi import UploadFile
from sqlalchemy import delete
from starlette.datastructures import UploadFile as StarletteUploadFile, Headers

from appodus_utils import BaseEntity
from appodus_utils.db.session import create_new_db_session


def create_mock_upload_file(filename: str = "test.txt", content: bytes = b"test content",
                            content_type: str = "application/pdf") -> UploadFile:
    file = BytesIO(content)
    headers = Headers({
        "content-type": content_type
    })
    upload_file = StarletteUploadFile(filename=filename, file=file, headers=headers)
    return upload_file


def get_real_temp_file_path():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        return tmp.name  # The file exists on disk until you manually delete it


async def truncate_entities(entities: List[Type[BaseEntity]]):
    async with create_new_db_session() as db_session:
        async with db_session.begin():
            for entity in entities:
                stmt = delete(entity)
                await db_session.execute(stmt)
