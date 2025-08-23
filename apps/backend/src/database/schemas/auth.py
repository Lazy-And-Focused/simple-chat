from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

# from .user import UserBase
from ..database import Base

class AuthBase(Base):
	__tablename__ = "auth"

	id: Mapped[int] = mapped_column(unique=True, primary_key=True)
	email: Mapped[str] = mapped_column(String(), unique=True)
	password: Mapped[str] = mapped_column(String())
	user_id: Mapped[str] = mapped_column(String())

	def __repr__(self) -> str:
		return f"""
AuthBase:\n{
"\n".join([f"{key}: {eval(f"self.{key}")}" for key in ["id", "user_id", "password", "email"]])
}
"""