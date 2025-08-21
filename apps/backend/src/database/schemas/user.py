from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from ..database import Base

class UserBase(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(nullable=False, unique=True, primary_key=True)
	user_name: Mapped[str] = mapped_column(String(30), unique=True)
	name: Mapped[Optional[str]] = mapped_column(String(30), default="none")
	avatar_url: Mapped[Optional[str]] = mapped_column(String(), default="none")

	def __repr__(self) -> str:
		return f"""
UserBase:\n{
"\n".join([f"{key}: {eval(f"self.{key}")}" for key in ["id", "user_name", "name", "avatar_url"]])
}
"""