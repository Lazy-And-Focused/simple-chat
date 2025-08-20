from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from ..database import Base

class RoomBase(Base):
	__tablename__ = "rooms"
	
	id: Mapped[int] = mapped_column(String(), primary_key=True)
	name: Mapped[str] = mapped_column(String(4096))
	icon: Mapped[Optional[str]] = mapped_column(String())
	messages: Mapped[str] = mapped_column(String())