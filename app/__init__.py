from flask import Flask
from .routes.main import main_bp
from .chat_db import init_db

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.secret_key = 'supersecret'

    # Initialize database on startup
    init_db()
    app.register_blueprint(main_bp)

    return app
