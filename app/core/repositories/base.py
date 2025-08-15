from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.core.db_helper import db_helper


class BaseRepository:
    def __init__(self, model, db=db_helper.session_getter):
        self.db = db
        self.model = model

    async def get_by_id_or_none(self, item_id: UUID):
        async with self.db() as session:
            query = await session.execute(select(self.model).filter_by(id=item_id))
            result = query.scalar_one_or_none()
            return result
