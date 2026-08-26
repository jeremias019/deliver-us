import os


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

    # --- Database ---
    # Local dev: plain SQLite file.
    # Production: point DATABASE_URL at Turso / Postgres / etc.
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///safe_and_sound.db")

    # --- Telegram ---
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

    # --- Admin auth (very basic — swap for something real before going public) ---
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
