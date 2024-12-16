from sqlalchemy.orm import Session
from api.core.decorators import handle_sqlalchemy_errors    
from api.v1.models import ContextModel
from api.v1.context.schemas import ContextCreateSchema, ContextUpdateSchema
from decouple import config as decouple_config

PAGE_SIZE = decouple_config("PAGE_SIZE")

class ContextServices:

    def _not_deleted(self, db: Session):
        return db.query(ContextModel).filter(ContextModel.is_deleted == False)

    @handle_sqlalchemy_errors
    def add(self, db: Session, obj: ContextCreateSchema):
        novo = ContextModel()
        novo.populate(obj)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo

    @handle_sqlalchemy_errors
    def get_all(self, db: Session, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        objs = self._not_deleted(db).order_by(ContextModel.name.asc()).limit(page_size).offset(offset).all()
        return objs

    @handle_sqlalchemy_errors
    def get_by_id(self, db: Session, id: str):
        return self._not_deleted(db).filter(ContextModel.id == id).first()

    @handle_sqlalchemy_errors
    def get_by_nome(self, db: Session, name: str, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        return self._not_deleted(db).filter(ContextModel.name.ilike(f"%{name}%")).limit(page_size).offset(offset).all()

    @handle_sqlalchemy_errors
    def update(self, db: Session, obj_to_update: ContextModel, data: ContextUpdateSchema):
        obj_to_update.populate(data)
        db.commit()
        db.refresh(obj_to_update)

    @handle_sqlalchemy_errors
    def delete(self, db: Session, id: str):
        obj = self._not_deleted(db).filter(ContextModel.id == id).first()
        obj.is_deleted = True
        db.commit()
        db.refresh(obj)
        return id


context_services = ContextServices()