from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Cart, Product

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart"
)
@cart_bp.route("", methods=["POST"])
@jwt_required()
def add_to_cart():

    data = request.get_json()

    user_id = int(get_jwt_identity())

    product = Product.query.get(data["product_id"])

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=data["product_id"]
    ).first()

    if cart_item:
        cart_item.quantity += data["quantity"]
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=data["product_id"],
            quantity=data["quantity"]
        )

        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": "Product added to cart"
    }), 201
@cart_bp.route("", methods=["GET"])
@jwt_required()
def get_cart():

    user_id = int(get_jwt_identity())

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    result = []

    total = 0

    for item in cart_items:

        subtotal = item.product.price * item.quantity

        total += subtotal

        result.append({
            "cart_id": item.id,
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return jsonify({
        "items": result,
        "grand_total": total
    }), 200

@cart_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_cart(id):

    cart = Cart.query.get(id)

    if not cart:
        return jsonify({
            "message": "Cart item not found"
        }),404

    data = request.get_json()

    cart.quantity = data["quantity"]

    db.session.commit()

    return jsonify({
        "message":"Cart updated successfully"
    }),200
@cart_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_cart(id):

    cart = Cart.query.get(id)

    if not cart:
        return jsonify({
            "message":"Cart item not found"
        }),404

    db.session.delete(cart)

    db.session.commit()

    return jsonify({
        "message":"Item removed from cart"
    }),200