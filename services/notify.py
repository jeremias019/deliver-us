import requests
from flask import current_app


def send_telegram(message: str) -> bool:
    """
    Send a plain-text (HTML-formatted) notification via Telegram.
    Returns True on success, False on failure — failures are logged,
    not raised, so a Telegram hiccup never blocks a delivery confirmation.
    """
    token = current_app.config["TELEGRAM_TOKEN"]
    chat_id = current_app.config["TELEGRAM_CHAT_ID"]

    if not token or not chat_id:
        current_app.logger.warning("Telegram not configured — skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        resp = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=5,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        current_app.logger.error(f"Telegram notification failed: {e}")
        return False


# TODO (you): customize the message content/format for each event type.
# Suggested call sites:
#   - When a delivery is marked complete (driver route)
#   - Optionally: when a driver logs an unplanned delivery via /log
def build_completion_message(delivery) -> str:
    """Example message builder — adjust wording/fields freely."""
    return (
        f"✅ <b>Delivery completed</b>\n"
        f"Courier: {delivery.courier or 'Unknown'}\n"
        f"Time: {delivery.completed_at.strftime('%Y-%m-%d %H:%M')} UTC\n"
        f"Source: {delivery.source}"
    )
