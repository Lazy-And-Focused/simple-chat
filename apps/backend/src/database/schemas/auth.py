from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

# from .user import UserBase
from ..database import Base

class AuthBase(Base):
	__tablename__ = "auth"

	id: Mapped[int] = mapped_column(String(), primary_key=True)
	user_id: Mapped[str] = mapped_column(String())
	password: Mapped[str] = mapped_column(String())
	email: Mapped[str] = mapped_column(String(), primary_key=True)

	def __repr__(self) -> str:
		return f"""
AuthBase:\n{
"\n".join([f"{key}: {eval(f"self.{key}")}" for key in ["id", "user_id", "password", "email"]])
}
"""