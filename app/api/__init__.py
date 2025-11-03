# app/api/__init__.py
from flask import Blueprint, jsonify
from flask import request, jsonify, abort

from ..helpers.helper import date_to_unix_ms
from ..models import Author
from ..models.base import db
from .utils import model_to_dict, paginate_query

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.get('/authors')
def list_authors():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    q = Author.query
    if name := request.args.get('q'):
        q = q.filter(Author.name.like('%' + name + '%'))
    items, meta = paginate_query(q, page, per_page)
    return jsonify({"data": [model_to_dict(a) for a in items], "meta": meta})


@api_bp.post('/authors')
def create_author():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    bio = (payload.get("bio") or "").strip()
    birth_date = (payload.get("birth_date") or "").strip()

    a = Author(name=name, bio=bio, birth_date=date_to_unix_ms(birth_date))

    db.session.add(a)
    db.session.commit()
    return jsonify(model_to_dict(a)), 201
