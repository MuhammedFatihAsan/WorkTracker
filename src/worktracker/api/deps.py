from fastapi import Depends
from sqlmodel import Session
from ..core.db import get_session

def get_db(session: Session = Depends(get_session)) -> Session:
    """
    FastAPI dependency: request başına bir Session enjekte eder.
    Response dönerken Session otomatik kapanır (get_session içinde context manager var).
    """
    return session
