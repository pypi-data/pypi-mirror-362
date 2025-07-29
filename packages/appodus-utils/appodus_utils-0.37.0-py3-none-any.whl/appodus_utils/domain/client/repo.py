from typing import Type

from sqlalchemy import select, literal

from appodus_utils.db.repo import GenericRepo
from kink import inject
from sqlalchemy.ext.asyncio import AsyncSession

from appodus_utils.domain.client.models import Client, CreateClientDto, UpdateClientDto, QueryClientDto, SearchClientDto


@inject
class ClientRepo(GenericRepo[Client, CreateClientDto, UpdateClientDto, QueryClientDto, SearchClientDto]):
    def __init__(self, db: AsyncSession, model: Type[Client] = Client, query_dto: Type[QueryClientDto] = QueryClientDto):
        super().__init__(db, model, query_dto)
        self.db = db


    async def exists_by_client_id(self, client_id: str) -> bool:
        stmt = select(literal(True)).where(
            self._model.deleted.is_(False),
            self._model.client_id == client_id
        )
        result = await self._session.execute(stmt)
        return result.scalar() is not None