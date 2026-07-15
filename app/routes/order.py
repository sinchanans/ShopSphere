from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import admin_required
from flask import request
from app.extensions import db
from app.models import Cart, Order, OrderItem

order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/orders"
)
@order_bp.route("", methods=["POST"])
@jwt_required()
def checkout():

    user_id = int(get_jwt_identity())

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({
            "message": "Cart is empty"
        }),400

    total_amount = 0

    for item in cart_items:
        total_amount += item.product.price * item.quantity

    order = Order(
        user_id=user_id,
        total_amount=total_amount
    )

    db.session.add(order)
    db.session.flush()

    for item in cart_items:

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )

        db.session.add(order_item)

        item.product.stock -= item.quantity

    Cart.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    return jsonify({
        "message":"Order placed successfully",
        "order_id":order.id,
        "total_amount":total_amount
    }),201
@order_bp.route("", methods=["GET"])
@jwt_required()
def get_orders():

    user_id = int(get_jwt_identity())

    orders = Order.query.filter_by(user_id=user_id).all()

    result = []

    for order in orders:

        result.append({
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at
        })

    return jsonify(result), 200
@order_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_order(id):

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message":"Order not found"
        }),404

    items=[]

    for item in order.items:

        items.append({
            "product":item.product.name,
            "price":item.price,
            "quantity":item.quantity
        })

    return jsonify({

        "order_id":order.id,

        "status":order.status,

        "total_amount":order.total_amount,

        "items":items

    }),200
@order_bp.route("/<int:id>", methods=["PUT"])
@admin_required
def update_status(id):

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message":"Order not found"
        }),404

    data=request.get_json()

    order.status=data["status"]

    db.session.commit()

    return jsonify({
        "message":"Order status updated"
    }),200