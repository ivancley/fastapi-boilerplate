import uuid
from datetime import datetime, timezone
from decouple import config as decouple_config
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from api.v1.user.schemas import UserCreateSchema
from api.v1.context.schemas import ContextCreateSchema

SCHEMA = decouple_config("SCHEMA")

@as_declarative()
class Base:
    __name__: str 

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    is_deleted = Column(
        Boolean, 
        default=False, 
        nullable=False, 
    )
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


user_context = Table(
    "user_context",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"), primary_key=True),
    Column("context_id", UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.contexts.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("user_id", "context_id", name="uq_user_context"),
    schema=SCHEMA
)


class ContextModel(Base):
    __tablename__ = 'contexts'
    __table_args__ = (
        UniqueConstraint("name", name="uq_context_name"),
        Index("ix_context_name", "name", unique=False),
        {"schema": SCHEMA},
    )

    name = Column(
        String(60), 
        nullable=False, 
        index=True, 
    )

    users = relationship(
        "UserModel",
        secondary=user_context,
        back_populates="contexts"
    )

    def populate(self, obj: ContextCreateSchema):
        if obj.name:
            self.name = obj.name
        return self


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        Index("ix_user_email", "email"),
        {"schema": SCHEMA},
    )

    name = Column(
        String(60),
        nullable=False,
        index=True
    )
    full_name = Column(
        String(120),
        nullable=False,
        index=True
    )
    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )
    phone = Column(
        String(20),
        nullable=True
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    password_hash = Column(
        String(128),
        nullable=False
    )

    contexts = relationship(
        "ContextModel",
        secondary=user_context,
        back_populates="users"
    )

    def populate(self, obj: UserCreateSchema):
        if obj.name is not None:
            self.name = obj.name
        if obj.full_name is not None:
            self.full_name = obj.full_name
        if obj.email is not None:
            self.email = obj.email
        if obj.phone:
            self.phone = obj.phone
        if obj.is_active is not None:
            self.is_active = obj.is_active
        if obj.password_hash is not None:
            self.password_hash = obj.password_hash
        return self
