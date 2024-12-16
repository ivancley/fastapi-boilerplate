from pydantic import BaseModel
from typing import Optional
import uuid

class ContextBaseSchema(BaseModel):
    name: str

class ContextCreateSchema(ContextBaseSchema):
    pass

class ContextUpdateSchema(ContextBaseSchema):
    name: Optional[str] = None

class ContextViewSchema(ContextBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True
