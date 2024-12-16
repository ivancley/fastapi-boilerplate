from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from api.v1.database import get_db
from api.v1.models import ContextModel
from api.v1.context.schemas import ContextCreateSchema, ContextUpdateSchema, ContextViewSchema
from api.v1.context.services import context_services as service

router = APIRouter(
    prefix="/api/v1/contextos",
    tags=["Contextos"],
)

exception_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado"
)


@router.get("/", response_model=List[ContextViewSchema])
def get_all(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
):
    objs = service.get_all(db=db, page=page, page_size=limit)
    return objs


@router.get("/{id}", response_model=ContextViewSchema)
def get_by_id(id: str, db: Session = Depends(get_db)):
    obj = service.get_by_id(db, id)
    if not obj:
        raise exception_not_found

    return obj


@router.get("/nome/{nome}", response_model=List[ContextViewSchema])
def get_by_nome(nome: str, db: Session = Depends(get_db)):
    return service.get_by_nome(db, nome)


@router.post("/", response_model=ContextViewSchema, status_code=status.HTTP_201_CREATED)
def create(obj_to_create: ContextCreateSchema, db: Session = Depends(get_db)):
    novo = service.add(db, obj_to_create)
    return novo


@router.put("/{id}", response_model=ContextViewSchema)
def update(id: str, data: ContextUpdateSchema, db: Session = Depends(get_db)):
    obj_to_update = service.get_by_id(db, id)
    if not obj_to_update:
        raise exception_not_found

    service.update(db, obj_to_update, data)
    return obj_to_update


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str, db: Session = Depends(get_db)):
    obj_to_delete = service.get_by_id(db, id)
    if not obj_to_delete:
        raise exception_not_found

    service.delete(db, id)
    return obj_to_delete
