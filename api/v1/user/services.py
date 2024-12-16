from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.future import select
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession 
from api.core.decorators import handle_sqlalchemy_errors    
from api.v1.models import UserModel, ContextModel
from api.v1.user.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema
from decouple import config as decouple_config
from api.core.exceptions import ExceptionNotFound

PAGE_SIZE = decouple_config("PAGE_SIZE")

class UserServices:

    def _not_deleted(self):
        return select(UserModel).filter(UserModel.is_deleted == False)
    
    async def _fetch_all(self, db: AsyncSession, query):
        result = await db.execute(query)
        return result.scalars().all()
    
    async def _fetch_one(self, db: AsyncSession, query):
        result = await db.execute(query)  
        return result.scalars().first() 

    @handle_sqlalchemy_errors
    async def add(self, db: AsyncSession, obj: UserCreateSchema):
        if not obj.context_ids or len(obj.context_ids) == 0:
            raise ValueError("Pelo menos um 'context_id' deve ser fornecido para associar o usuário a um contexto.")
        
        new_obj = UserModel().populate(obj)  

        if obj.context_ids and len(obj.context_ids) > 0:
            query = select(ContextModel).filter(ContextModel.id.in_(obj.context_ids))
            contexts = await self._fetch_all(db, query)  
            new_obj.contexts = contexts

        db.add(new_obj)  
        await db.commit()  
        await db.refresh(new_obj)  
        return UserViewSchema.model_validate(new_obj, from_attributes=True)  
        
    @handle_sqlalchemy_errors
    async def get_all(self, db: AsyncSession, page: int = 1, page_size: int = PAGE_SIZE) -> List[UserViewSchema]:
        offset = (page - 1) * page_size
        query = self._not_deleted().options(selectinload(UserModel.contexts)).offset(offset).limit(page_size)
        objs = await self._fetch_all(db, query) 
        return [UserViewSchema.model_validate(obj, from_attributes=True) for obj in objs] 
    
    @handle_sqlalchemy_errors
    async def get_by_id(self, db: AsyncSession, id: str) -> UserViewSchema:
        query = self._not_deleted().options(selectinload(UserModel.contexts)).filter(UserModel.id == id.strip())
        obj = await self._fetch_one(db, query)
        if obj is None:
            raise ExceptionNotFound()
        return UserViewSchema.model_validate(obj, from_attributes=True) 

    @handle_sqlalchemy_errors
    async def get_by_nome(self, db: AsyncSession, name: str, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        result = await db.execute(self._not_deleted(db).filter(UserModel.name.ilike(name)).limit(page_size).offset(offset))
        return result.scalars().all()

    @handle_sqlalchemy_errors
    async def update(self, db: AsyncSession, obj_to_update: UserModel, data: UserUpdateSchema):
        obj_to_update.populate(data)
    
        if data.context_ids:
            query = select(ContextModel).filter(ContextModel.id.in_(data.context_ids))
            contexts = await self._fetch_all(db, query) 
            obj_to_update.contexts = contexts 

        await db.commit()  
        await db.refresh(obj_to_update) 
        return UserViewSchema.model_validate(obj_to_update, from_attributes=True)

    @handle_sqlalchemy_errors
    async def delete(self, db: AsyncSession, id: str):
        obj = await self.get_by_id(db, id)
        obj.is_deleted = True
        await db.commit()
        await db.refresh(obj)
        return id


user_services = UserServices()