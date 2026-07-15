from app.extensions import db


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref="orders"
    )