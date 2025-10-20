from flask import Blueprint, render_template, request, redirect, url_for

from .. import db
from ..models import Author

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


@authors_bp.get("/")
def index():
    q = (request.args.get("q") or "").strip()
    query = Author.query
    if q:
        like = f"%{q}%"
        query = query.filter((Author.name.ilike(like)) | (Author.bio.ilike(like)))
    authors = query.order_by(Author.name.asc()).all()
    return render_template("authors/index.html", authors=authors, q=q)


@authors_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        bio = (request.form.get("bio") or "").strip()
        if not name:
            return render_template("authors/edit.html", author=None, error="Name is required",
                                   form={"name": name, "bio": bio})
        a = Author(name=name, bio=bio or None)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("authors.index"))
    return render_template("authors/edit.html", author=None)


@authors_bp.route("/<int:author_id>/edit", methods=["GET", "POST"])
def edit(author_id):
    author = Author.query.get_or_404(author_id)
    if request.method == "POST":
        if request.form.get("_action") == "delete":
            db.session.delete(author)
            db.session.commit()
            return redirect(url_for("authors.index"))
        name = (request.form.get("name") or "").strip()
        bio = (request.form.get("bio") or "").strip()
        if not name:
            return render_template("authors/edit.html", author=author, error="Name is required")
        author.name = name
        author.bio = bio or None
        db.session.commit()
        return redirect(url_for("authors.index"))
    return render_template("authors/edit.html", author=author)
