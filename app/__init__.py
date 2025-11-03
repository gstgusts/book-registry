from flask import Flask, render_template

from .models import Author, Book, Order
from .models.base import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register web blueprints (split by entity)
    from .web.authors import authors_bp
    from .web.books import books_bp
    from .web.orders import orders_bp
    app.register_blueprint(authors_bp)  # /authors
    app.register_blueprint(books_bp)  # /books
    app.register_blueprint(orders_bp)  # /orders

    # Register api endpoints
    from .api import api_bp
    app.register_blueprint(api_bp)

    @app.get("/")
    def home():
        return render_template(
            "home.html",
            author_count=Author.query.count(),
            book_count=Book.query.count(),
            order_count=Order.query.count(),
        )

    return app
