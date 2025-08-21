from sqlalchemy import create_engine

from .schemas import AuthBase, MessageBase, UserBase, RoomBase
from .database import Base
from .constants import DATABASE_URL

engine = create_engine(DATABASE_URL)

def createTables() -> None:
	Base.metadata.create_all(engine)
	AuthBase.metadata.create_all(engine)
	MessageBase.metadata.create_all(engine)
	RoomBase.metadata.create_all(engine)
	UserBase.metadata.create_all(engine)