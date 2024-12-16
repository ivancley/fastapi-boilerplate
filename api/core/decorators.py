# app/core/decorators.py
from functools import wraps
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DatabaseError,
    DataError,
    ProgrammingError,
    InvalidRequestError,
    InterfaceError,
    TimeoutError,
    NoResultFound,
    MultipleResultsFound,
    SQLAlchemyError,
)
from sqlalchemy.orm import Session
from typing import Callable
from api.core.exceptions import (
    ExceptionBadRequest,
    ExceptionNotFound,
    ExceptionInternalServerError,
)


def handle_sqlalchemy_errors(func):
    @wraps(func)
    def wrapper(self, db: Session, *args, **kwargs):
        try:
            return func(self, db, *args, **kwargs)
        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Erro de integridade: {str(e.orig)}")
        except OperationalError as e:
            db.rollback()
            raise ValueError(f"Erro de conexão com o banco de dados: {str(e)}")
        except DatabaseError as e:
            db.rollback()
            raise ValueError(f"Erro no banco de dados: {str(e)}")
        except DataError as e:
            db.rollback()
            raise ValueError(f"Erro de dados: {str(e)}")
        except ProgrammingError as e:
            db.rollback()
            raise ValueError(f"Erro de sintaxe: {str(e)}")
        except InvalidRequestError as e:
            db.rollback()
            raise ValueError(f"Erro de solicitação inválida: {str(e)}")
        except InterfaceError as e:
            db.rollback()
            raise ValueError(f"Erro de interface: {str(e)}")
        except TimeoutError as e:
            db.rollback()
            raise ValueError(f"Erro de timeout: {str(e)}")
        except NoResultFound as e:
            db.rollback()
            raise ValueError(f"Nenhum resultado encontrado: {str(e)}")
        except MultipleResultsFound as e:
            db.rollback()
            raise ValueError(f"Múltiplos resultados encontrados: {str(e)}")
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Erro no SQLAlchemy: {str(e)}")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Erro inesperado: {str(e)}")

    return wrapper


