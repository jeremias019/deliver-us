from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, current_app, Response, flash
)

from models import Delivery
from services.qr import generate_qr_png

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---- Very basic session-based auth ----

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == current_app.config["ADMIN_PASSWORD"]:
            session["is_admin"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Incorrect password.")
    return render_template("admin_login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def create():
    """Create a new expected delivery and generate its QR code."""
    if request.method == "POST":
        # TODO (you): add validation as needed (required fields, date format, etc.)
        delivery = Delivery.create(
            courier=request.form.get("courier"),
            expected_date=request.form.get("expected_date"),
            instructions=request.form.get("instructions"),
            source="planned",
        )
        return redirect(url_for("admin.show_qr", token=delivery.token))

    return render_template("admin_create.html")


@admin_bp.route("/qr/<token>")
@login_required
def show_qr(token):
    """Printable/mobile-friendly page displaying the QR for one delivery."""
    delivery = Delivery.get_by_token(token)
    if not delivery:
        return "Delivery not found", 404

    delivery_url = f"{current_app.config['BASE_URL']}/d/{delivery.token}"
    return render_template("qr_display.html", delivery=delivery, delivery_url=delivery_url)


@admin_bp.route("/qr/<token>.png")
@login_required
def qr_image(token):
    """Raw PNG for the QR code, embedded via <img src=...> in qr_display.html."""
    delivery = Delivery.get_by_token(token)
    if not delivery:
        return "Delivery not found", 404

    delivery_url = f"{current_app.config['BASE_URL']}/d/{delivery.token}"
    png_bytes = generate_qr_png(delivery_url)
    return Response(png_bytes, mimetype="image/png")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    """History of all deliveries, pending and completed."""
    deliveries = Delivery.all_ordered()
    return render_template("admin_dashboard.html", deliveries=deliveries)


@admin_bp.route("/qr/static")
@login_required
def show_static_qr():
    """
    Printable/mobile-friendly page for the ONE permanent door QR that points
    at /log — used when a delivery wasn't pre-logged. This never changes,
    so print it once and leave it up.
    """
    log_url = f"{current_app.config['BASE_URL']}/log"
    return render_template("qr_static_display.html", log_url=log_url)


@admin_bp.route("/qr/static.png")
@login_required
def static_qr_image():
    """Raw PNG for the static /log QR code."""
    log_url = f"{current_app.config['BASE_URL']}/log"
    png_bytes = generate_qr_png(log_url)
    return Response(png_bytes, mimetype="image/png")
