from contextvars import ContextVar
from http.client import HTTPException
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from .sessions import Session

session_context_var: ContextVar[Optional[Session]] = ContextVar("_session", default=None)


def set_db():
    db = Session()
    try:
        yield
    except (SQLAlchemyError, HTTPException) as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db() -> Session:
    session = Session()
    if session is None:
        raise Exception("Session is missing")
    return session
