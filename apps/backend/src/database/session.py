from typing import TypeVar, Generic, Any, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select 

from .engine import engine, createTables

createTables()

Session = sessionmaker(engine)
session = Session()

T = TypeVar("T")

class Database(Generic[T]):
    _base: type[T]

    def __init__(self, base: type[T]) -> None:
        super().__init__()
        
        self._base = base

    def create(self, data: T) -> None:
        try:
            created = session.add(data)
            session.commit()

            return created
        except:
            session.rollback()
            session.commit()
            raise


    def update(self, data: T):
        try:
            data = session.merge(data)
            session.commit()

            return data
        except:
            session.rollback()
            session.commit()
            raise

    def getById(self, id: int) -> T:
        try:
            statement = select(self._base).where(self._base.id == id) # type: ignore
            data = session.scalars(statement).one() # type: ignore

            return data
        except:
            raise

    def getByKey(self, key: str, data: Any) -> Sequence[T]:
        try:
            statement = select(self._base).where(eval(f"self._base.{key}") == data) #type: ignore
            getted = session.scalars(statement).all()
            
            return getted
        except:
            raise

    def delete(self, id: int):
        try:
            data = session.delete(self.getById(id))
            session.commit()

            return data
        except:
            session.rollback()
            session.commit()
            raise