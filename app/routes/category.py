from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Category
from app.decorators import admin_required

category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="/categories"
)


# ----------------------------
# Create Category
# ----------------------------
@category_bp.route("", methods=["POST"])
@admin_required
def create_category():

    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data"}), 400

    existing = Category.query.filter_by(
        name=data["name"]
    ).first()

    if existing:
        return jsonify({
            "message": "Category already exists"
        }), 400

    category = Category(
        name=data["name"],
        description=data.get("description")
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully"
    }), 201


# ----------------------------
# Get All Categories
# ----------------------------
@category_bp.route("", methods=["GET"])
def get_categories():

    categories = Category.query.all()

    result = []

    for category in categories:

        result.append({
            "id": category.id,
            "name": category.name,
            "description": category.description
        })

    return jsonify(result), 200