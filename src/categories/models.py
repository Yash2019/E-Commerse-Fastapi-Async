from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.db.main import Base
from datetime import datetime

class Categories(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id', ondelete='RESTRICT'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    parent = relationship("Categories",remote_side=[id],backref="children")
    