from sqlalchemy.orm import Session, joinedload, selectinload
from uuid import UUID
from api.core.decorators import handle_sqlalchemy_errors    
from api.v1.models import UserModel, ContextModel
from api.v1.user.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema
from decouple import config as decouple_config

PAGE_SIZE = decouple_config("PAGE_SIZE")

class UserServices:

    def _not_deleted(self, db: Session):
        return db.query(UserModel).filter(UserModel.is_deleted == False)
    
    def _get_user_contexts(self, db: Session):
        return self._not_deleted(db).options(
            joinedload(UserModel.contexts)
        )

    @handle_sqlalchemy_errors
    def add(self, db: Session, obj: UserCreateSchema):
        if not obj.context_ids or len(obj.context_ids) == 0:
            raise ValueError("Pelo menos um 'context_id' deve ser fornecido para associar o usuário a um contexto.")
            
        novo_user = UserModel().populate(obj)

        if obj.context_ids and len(obj.context_ids) > 0:
            contexts = db.query(ContextModel).filter(ContextModel.id.in_(obj.context_ids)).all()
            novo_user.contexts = contexts
       
        db.add(novo_user)
        db.commit()
        db.refresh(novo_user)
        return novo_user
        
        
    @handle_sqlalchemy_errors
    def get_all(self, db: Session, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        users = self._not_deleted(db).offset(offset).limit(page_size).all()
        return [UserViewSchema.from_orm(user) for user in users]
    
    @handle_sqlalchemy_errors
    def get_by_id(self, db: Session, id: str):
        return self._not_deleted(db).filter(UserModel.id == id.strip()).first()

    @handle_sqlalchemy_errors
    def get_by_nome(self, db: Session, name: str, page: int = 1, page_size: int = PAGE_SIZE):
        offset = (page - 1) * page_size
        return self._not_deleted(db).filter(UserModel.name.ilike(f"%{name}%")).limit(page_size).offset(offset).all()

    @handle_sqlalchemy_errors
    def update(self, db: Session, obj_to_update: UserModel, data: UserUpdateSchema):
        obj_to_update.populate(data)
        db.commit()
        db.refresh(obj_to_update)

    @handle_sqlalchemy_errors
    def delete(self, db: Session, id: str):
        obj = self.get_by_id(db, id)
        obj.is_deleted = True
        db.commit()
        db.refresh(obj)
        return id


user_services = UserServices()