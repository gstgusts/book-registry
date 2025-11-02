from app.models.base import db


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    published_year = db.Column(db.Integer)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
    )
    description = db.Column(db.Text)
    author = db.relationship("Author", back_populates="books")
    # order_items = db.relationship(
    #     "OrderItem",
    #     back_populates="order",
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    # )
