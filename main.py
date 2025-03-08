from flask import Flask
from routes.api import api_bp
from routes.web import web_bp

app = Flask(__name__)

# Register blueprint for routes
app.register_blueprint(web_bp)
app.register_blueprint(api_bp, url_prefix="/api")


if __name__ == "__main__":
    app.run(debug=True)
