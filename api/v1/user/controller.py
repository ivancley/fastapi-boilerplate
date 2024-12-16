from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from api.v1.database import get_db
from api.core.decorators import ExceptionBadRequest, ExceptionNotFound
from api.v1.user.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema
from api.v1.user.services import user_services as service

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["Users"]
)

@router.get("/", response_model=List[UserViewSchema])
def get_all(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
):
    objs = service.get_all(db=db, page=page, page_size=limit)
    return objs


@router.get("/{id}", response_model=UserViewSchema)
def get_by_id(id: str, db: Session = Depends(get_db)):
    obj = service.get_by_id(db, id)
    if not obj:
        raise ExceptionNotFound

    return obj


@router.get("/nome/{nome}", response_model=List[UserViewSchema])
def get_by_nome(nome: str, db: Session = Depends(get_db)):
    try:
        return service.get_by_nome(db, nome)
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.post("/", response_model=UserViewSchema, status_code=status.HTTP_201_CREATED)
def create(obj_to_create: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        novo = service.add(db, obj_to_create)
        return novo
    except ValueError as e:
        raise ExceptionBadRequest(detail=str(e)) 
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.put("/{id}", response_model=UserViewSchema)
def update(id: str, data: UserUpdateSchema, db: Session = Depends(get_db)):
    try:
        obj_to_update = service.get_by_id(db, id)
        if not obj_to_update:
            raise ExceptionNotFound()

        service.update(db, obj_to_update, data)
        return obj_to_update
    
    except ValueError as e:
        raise ExceptionBadRequest(detail=str(e)) 
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str, db: Session = Depends(get_db)):
    try:
        obj_to_delete = service.get_by_id(db, id)
        if not obj_to_delete:
            raise ExceptionNotFound

        service.delete(db, id)
        return obj_to_delete
    except ValueError as e:
        raise ExceptionBadRequest(detail=str(e)) 
    except Exception as e:
        raise ExceptionBadRequest(detail=str(e))
