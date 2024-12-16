from decouple import config as decouple_config
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.core.decorators import handle_sqlalchemy_errors
from api.core.exceptions import ExceptionNotFound    
from api.v1.models import ContextModel
from api.v1.context.schemas import ContextCreateSchema, ContextUpdateSchema, ContextViewSchema

PAGE_SIZE = decouple_config("PAGE_SIZE")

class ContextServices:

    def _not_deleted(self):
        return select(ContextModel).filter(ContextModel.is_deleted == False)
    
    async def _fetch_all(self, db: AsyncSession, query):
        result = await db.execute(query)
        return result.scalars().all()
    
    async def _fetch_one(self, db: AsyncSession, query):
        result = await db.execute(query)  
        return result.scalars().first() 

    @handle_sqlalchemy_errors
    async def add(self, db: AsyncSession, obj: ContextCreateSchema):
    
        db.add(obj)  
        await db.commit()  
        await db.refresh(obj)  
        return ContextViewSchema.model_validate(obj, from_attributes=True)  
        
    @handle_sqlalchemy_errors
    async def get_all(self, db: AsyncSession, page: int = 1, page_size: int = PAGE_SIZE) -> List[ContextViewSchema]:
        offset = (page - 1) * page_size
        query = self._not_deleted().options(selectinload(ContextModel.contexts)).offset(offset).limit(page_size)
        objs = await self._fetch_all(db, query) 
        return [ContextViewSchema.model_validate(obj, from_attributes=True) for obj in objs] 
    
    @handle_sqlalchemy_errors
    async def get_by_id(self, db: AsyncSession, id: str) -> ContextViewSchema:
        query = self._not_deleted().options(selectinload(ContextModel.contexts)).filter(ContextModel.id == id.strip())
        obj = await self._fetch_one(db, query)
        if obj is None:
            raise ExceptionNotFound()
        return ContextViewSchema.model_validate(obj, from_attributes=True) 

    @handle_sqlalchemy_errors
    async def get_by_nome(self, db: AsyncSession, name: str, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        result = await db.execute(self._not_deleted(db).filter(ContextModel.name.ilike(name)).limit(page_size).offset(offset))
        return result.scalars().all()

    @handle_sqlalchemy_errors
    async def update(self, db: AsyncSession, obj_to_update: ContextModel, data: ContextUpdateSchema):
        obj_to_update.populate(data)
    
        if data.context_ids:
            query = select(ContextModel).filter(ContextModel.id.in_(data.context_ids))
            contexts = await self._fetch_all(db, query) 
            obj_to_update.contexts = contexts 

        await db.commit()  
        await db.refresh(obj_to_update) 
        return ContextViewSchema.model_validate(obj_to_update, from_attributes=True)

    @handle_sqlalchemy_errors
    async def delete(self, db: AsyncSession, id: str):
        obj = await self.get_by_id(db, id)
        obj.is_deleted = True
        await db.commit()
        await db.refresh(obj)
        return id


context_services = ContextServices()
