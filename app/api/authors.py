# from flask import request, jsonify, abort
# from . import api_bp
# from ..models import Author
# from ..models.base import db
# from .utils import model_to_dict, paginate_query
#
#
# @api_bp.get('/authors')
# def list_authors():
#     page = int(request.args.get('page', 1))
#     per_page = int(request.args.get('per_page', 20))
#     q = Author.query
#     if name := request.args.get('q'):
#         q = q.filter(Author.name.like('%' + name + '%'))
#         items, meta = paginate_query(q, page, per_page)
#         return jsonify({"data":[model_to_dict(a) for a in items], "meta": meta})
