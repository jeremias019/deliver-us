import secrets
import string
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def generate_token(length: int = 12) -> str:
    """URL-safe random token used in the QR code link."""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False, index=True)

    courier = db.Column(db.String(120), nullable=True)
    expected_date = db.Column(db.String(20), nullable=True)  # store as ISO date string, keep it simple
    instructions = db.Column(db.Text, nullable=True)

    # pending -> completed
    status = db.Column(db.String(20), nullable=False, default="pending")

    # Was this pre-created by the admin, or logged on the spot by the driver via /log ?
    source = db.Column(db.String(20), nullable=False, default="planned")  # "planned" | "on_the_spot"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # ---- Helpers ----
    # TODO (you): flesh these out / add fields as you see fit (e.g. photo proof,
    # delivery notes left by the driver, courier company logo, etc.)

    @staticmethod
    def create(courier=None, expected_date=None, instructions=None, source="planned"):
        delivery = Delivery(
            token=generate_token(),
            courier=courier,
            expected_date=expected_date,
            instructions=instructions,
            source=source,
        )
        db.session.add(delivery)
        db.session.commit()
        return delivery

    @staticmethod
    def get_by_token(token: str):
        return Delivery.query.filter_by(token=token).first()

    def mark_complete(self):
        self.status = "completed"
        self.completed_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def all_ordered():
        return Delivery.query.order_by(Delivery.created_at.desc()).all()
