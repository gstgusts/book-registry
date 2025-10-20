from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.get("/")
def index():
    q = (request.args.get("q") or "").strip()
    query = Order.query
    if q:
        like = f"%{q}%"
        query = query.filter((Order.number.ilike(like)))
    orders = query.order_by(Order.number.asc()).all()
    return render_template("orders/index.html", orders=orders, q=q)
