from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return {
            "message": "Welcome to ShopSphere API"
        }

    return app