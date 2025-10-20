from flask import Blueprint, render_template, request, redirect, url_for

from .. import db
from ..models import Book, Author

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.get("/")
def index():
    title = (request.args.get("title") or "").strip()
    author = (request.args.get("author") or "").strip()

    query = Book.query.join(Author)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Author.name.ilike(f"%{author}%"))

    books = query.order_by(Book.title.asc()).all()
    authors = Author.query.order_by(Author.name.asc()).all()
    return render_template("books/index.html", books=books, title=title, author=author, authors=authors)


@books_bp.route("/new", methods=["GET", "POST"])
def new():
    authors = Author.query.order_by(Author.name.asc()).all()
    if not authors:
        return redirect(url_for("authors.new"))

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        published_year = request.form.get("published_year")
        author_id = request.form.get("author_id")
        if not title:
            return render_template("books/edit.html", book=None, authors=authors, error="Title is required")
        if not author_id:
            return render_template("books/edit.html", book=None, authors=authors, error="Author is required")
        try:
            author_id = int(author_id)
        except ValueError:
            return render_template("books/edit.html", book=None, authors=authors, error="Invalid author")
        b = Book(title=title, published_year=(int(published_year) if published_year else None), author_id=author_id)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for("books.index"))
    return render_template("books/edit.html", book=None, authors=authors)


@books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    authors = Author.query.order_by(Author.name.asc()).all()
    if request.method == "POST":
        if request.form.get("_action") == "delete":
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for("books.index"))
        title = (request.form.get("title") or "").strip()
        published_year = request.form.get("published_year")
        author_id = request.form.get("author_id")
        if not title:
            return render_template("books/edit.html", book=book, authors=authors, error="Title is required")
        try:
            author_id = int(author_id)
        except (TypeError, ValueError):
            return render_template("books/edit.html", book=book, authors=authors, error="Invalid author")
        book.title = title
        book.published_year = int(published_year) if published_year else None
        book.author_id = author_id
        db.session.commit()
        return redirect(url_for("books.index"))
    return render_template("books/edit.html", book=book, authors=authors)
