from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.decorators import ExceptionBadRequest, ExceptionNotFound
from api.v1.database import get_db
from api.v1.user.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema
from api.v1.user.services import user_services as service

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["Users"]
)

@router.get("/", response_model=List[UserViewSchema])
async def get_all(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
):
    objs = await service.get_all(db=db, page=page, page_size=limit)
    return objs


@router.get("/{id}", response_model=UserViewSchema)
async def get_by_id(id: str, db: AsyncSession = Depends(get_db)):
    obj = await service.get_by_id(db, id)
    if not obj:
        raise ExceptionNotFound

    return obj


@router.get("/nome/{nome}", response_model=List[UserViewSchema])
async def get_by_nome(nome: str, db: AsyncSession = Depends(get_db)):
    try:
        return await service.get_by_nome(db, nome) 
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.post("/", response_model=UserViewSchema, status_code=status.HTTP_201_CREATED)
async def create(obj_to_create: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        novo = await service.add(db, obj_to_create) 
        return novo
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.put("/{id}", response_model=UserViewSchema)
async def update(id: str, data: UserUpdateSchema, db: AsyncSession = Depends(get_db)):
    try:
        obj_to_update = await service.get_by_id(db, id) 
        if not obj_to_update:
            raise ExceptionNotFound()

        await service.update(db, obj_to_update, data) 
        return obj_to_update
    
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    try:
        obj_to_delete = await service.get_by_id(db, id) 
        if not obj_to_delete:
            raise ExceptionNotFound

        await service.delete(db, id) 
        return obj_to_delete

    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))
