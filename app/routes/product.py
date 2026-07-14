from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Product, Category
from app.decorators import admin_required

product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/products"
)
@product_bp.route("", methods=["POST"])
@admin_required
def create_product():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data"}), 400

    category = Category.query.get(data["category_id"])

    if not category:
        return jsonify({"message": "Category not found"}), 404

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data["stock"],
        image_url=data.get("image_url"),
        category_id=data["category_id"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully"
    }), 201
@product_bp.route("", methods=["GET"])
def get_products():

    products = Product.query.all()

    result = []

    for product in products:

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image_url": product.image_url,
            "category": product.category.name
        })

    return jsonify(result), 200
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "category": product.category.name
    }), 200
@product_bp.route("/<int:id>", methods=["PUT"])
@admin_required
def update_product(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.image_url = data.get("image_url", product.image_url)

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully"
    }), 200
@product_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete_product(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200