from sqlalchemy.orm import sessionmaker

from .schemas.utils import create
from .schemas import UserBase
from .engine import engine, createTables

createTables()

Session = sessionmaker(engine)
session = Session()

try:
    create(UserBase(user_name="fockusty"), session)
except:
    session.rollback()
    raise
else:
    session.commit()