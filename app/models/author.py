from app.models.base import db
from app.models.types import EpochMsDate


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)
    birth_date = db.Column(EpochMsDate, nullable=True)
    books = db.relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
