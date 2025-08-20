from typing import Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select 

from .schemas import UserBase
from .engine import engine, createTables

createTables()

Session = sessionmaker(engine)
session = Session()

def create(data: Any):
    return session.add(data)

def update(data: Any):
    return session.merge(data)

def getById(id: int, base: Any):
    statement = select(base).where(base.id == id) # type: ignore
    data = session.scalars(statement).one()

    return data

# def delete(id: str):


try:
    # create(UserBase(user_name="fockusty"))

    print(getById(1, UserBase))
except:
    session.rollback()
    raise
else:
    session.commit()