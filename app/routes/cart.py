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