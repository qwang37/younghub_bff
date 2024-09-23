from flask import Flask

from app.api.storage_auth import auth_bp
from app.api.video import video_bp
from app.api.cards import card_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management and flashing

app.register_blueprint(video_bp)
app.register_blueprint(card_bp)
app.register_blueprint(auth_bp)
from app import index  # Import the routes from cards.py