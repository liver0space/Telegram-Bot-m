from flask import Flask

from app.extensions import bootstrap, db, socketio
from app.routes import routes_bp

from .config import Config


def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static', static_url_path='/')
    app.config.from_object(Config)

    db.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)

    # Remove in production
    from app import models
    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    return app
