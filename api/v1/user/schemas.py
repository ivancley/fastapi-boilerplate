from pydantic import BaseModel
from typing import Optional, List
import uuid
from api.v1.context.schemas import ContextBaseSchema, ContextViewSchema

class UserBaseSchema(BaseModel):
    name: str
    full_name: Optional[str] = None
    email: str
    phone: Optional[str]
    is_active: bool

class UserCreateSchema(UserBaseSchema):
    context_ids: List[uuid.UUID]
    password_hash: str

class UserUpdateSchema(UserBaseSchema):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    context_ids: Optional[List[uuid.UUID]] = None
    password_hash: Optional[str] = None

class UserViewSchema(UserBaseSchema):
    id: uuid.UUID
    contexts: List[ContextViewSchema]

    class Config:
        from_attributes = True
