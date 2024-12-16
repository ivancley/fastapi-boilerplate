from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from decouple import config as decouple_config

# Conectar ao banco de dados
engine = create_async_engine(decouple_config("DATABASE_URL"), pool_pre_ping=True, echo=True)

# Criar a base para os models
Base: DeclarativeMeta = declarative_base()

# Sessão de conexão
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Função para obter a sessão
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
