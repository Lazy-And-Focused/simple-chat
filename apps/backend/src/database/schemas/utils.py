from typing import Any

from sqlalchemy.orm import Session

def create(data: Any, session: Session):
    session.add(data)