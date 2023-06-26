from http.client import HTTPException

from sqlalchemy.exc import SQLAlchemyError

from .sessions import Session


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
