from flask import Blueprint, render_template, redirect, url_for, request

from models import Delivery
from services.notify import send_telegram, build_completion_message

driver_bp = Blueprint("driver", __name__)


@driver_bp.route("/d/<token>", methods=["GET"])
def view_delivery(token):
    """What the driver sees after scanning the delivery-specific QR."""
    delivery = Delivery.get_by_token(token)
    if not delivery:
        return render_template("driver_not_found.html"), 404

    return render_template("driver_confirm.html", delivery=delivery)


@driver_bp.route("/d/<token>/complete", methods=["POST"])
def complete_delivery(token):
    """Driver pressed 'Delivery Complete'."""
    delivery = Delivery.get_by_token(token)
    if not delivery:
        return render_template("driver_not_found.html"), 404

    if delivery.status != "completed":
        delivery.mark_complete()
        send_telegram(build_completion_message(delivery))

    return render_template("driver_done.html", delivery=delivery)


@driver_bp.route("/log", methods=["GET", "POST"])
def log_on_the_spot():
    """
    Fallback flow for the static door QR: driver arrives, nothing was
    pre-logged, so they fill in the minimum themselves and get sent
    straight into the same confirm/complete flow.
    """
    if request.method == "POST":
        # TODO (you): decide which fields are required here vs optional
        delivery = Delivery.create(
            courier=request.form.get("courier"),
            expected_date=None,
            instructions=request.form.get("note"),
            source="on_the_spot",
        )
        return redirect(url_for("driver.view_delivery", token=delivery.token))

    return render_template("driver_log_form.html")
