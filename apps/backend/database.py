from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, create_engine

from constants import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
	pass

class AuthBase(Base):
	__tablename__ = "auth"

	id: Mapped[str] = mapped_column(String(), primary_key=True)
	user_id: Mapped[str] = mapped_column(String())
	password: Mapped[str] = mapped_column(String())
	email: Mapped[str] = mapped_column(String(), primary_key=True)

class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[str] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30))
	avatar_url: Mapped[str] = mapped_column(String())
	
class MessageBase(Base):
	__tablename__ = "messages"
	
	id: Mapped[str] = mapped_column(String(), primary_key=True)
	content: Mapped[str] = mapped_column(String(4096))
	sender_id: Mapped[str] = mapped_column(String())
	reply_id: Mapped[str] = mapped_column(String())
