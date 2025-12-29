from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from ..database import Base

class MessageBase(Base):
	__tablename__ = "messages"
	
	id: Mapped[int] = mapped_column(String(), primary_key=True)
	content: Mapped[str] = mapped_column(String(4096))
	sender_id: Mapped[str] = mapped_column(String())
	attacments: Mapped[Optional[str]] = mapped_column(String())
	reply_id: Mapped[Optional[str]] = mapped_column(String())

	def __repr__(self) -> str:
		return f"""
MessageBase:\n{
"\n".join([f"{key}: {eval(f"self.{key}")}" for key in ["id", "content", "sender_id", "attacments", "reply_id"]])
}
"""