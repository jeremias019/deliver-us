from flask import Flask

from config import Config
from models import db
from routes.admin import admin_bp
from routes.driver import driver_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Turso/libsql: pass the auth token explicitly via connect_args rather than
    # relying on it being parsed correctly out of the URL query string.
    if app.config["DATABASE_URL"].startswith("sqlite+libsql://") and app.config.get("TURSO_AUTH_TOKEN"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"auth_token": app.config["TURSO_AUTH_TOKEN"]}
        }

    db.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(driver_bp)

    with app.app_context():
        db.create_all()  # fine for SQLite/small scale; swap for migrations later if needed

    @app.route("/")
    def index():
        return "Safe and Sound is running. Visit /admin to manage deliveries."

    return app


app = create_app()

if __name__ == "__main__":
    # Local dev only — Render will run this via gunicorn (see Procfile)
    app.run(debug=True, port=5000)