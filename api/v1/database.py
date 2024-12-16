from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config as decouple_config

# Conectar ao banco de dados
engine = create_engine(decouple_config("DATABASE_URL"), pool_pre_ping=True, echo=True)

# Criar a base para os models
Base: DeclarativeMeta = declarative_base()

# Sessão de conexão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
