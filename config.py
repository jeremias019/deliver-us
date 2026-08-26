import os


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

    # --- Database ---
    # Local dev: plain SQLite file (default below).
    # Production (Turso): set DATABASE_URL to the bare host, e.g.
    #   sqlite+libsql://<db-name>-<org>.turso.io/?secure=true
    # and set TURSO_AUTH_TOKEN separately (passed via connect_args in app.py,
    # which is more reliable than embedding it in the URL query string).
    # Requires the sqlalchemy-libsql package (already in requirements.txt).
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///deliver-us.db")
    TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")

    # --- Telegram ---
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

    # --- Admin auth (very basic — swap for something real before going public) ---
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")