from flask import Flask
from app.videos.routes import video_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management and flashing

app.register_blueprint(video_bp)
from app import routes  # Import the routes from routes.py