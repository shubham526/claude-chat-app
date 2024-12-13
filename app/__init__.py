from flask import Flask
from config import Config
import anthropic
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Session
    Session(app)

    # Initialize Anthropic client with explicit API key
    app.claude_client = anthropic.Anthropic(api_key=app.config['ANTHROPIC_API_KEY'])

    from app.routes import main
    app.register_blueprint(main)

    return app

