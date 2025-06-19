from flask import Flask
from flask_cors import CORS
from API.routes.feedback_routes import feedback_bp
from API.routes.question_routes import question_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(question_bp)
    return app
