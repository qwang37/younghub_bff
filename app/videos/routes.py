from flask import Blueprint, render_template
from flask import jsonify

video_bp = Blueprint('videos', __name__)

@video_bp.route('/videos')
def list_videos():
    video_url = "https://younghubstorage.blob.core.windows.net/short-video"
    videos = [
        {"ID": 1, "VideoURL": video_url + "/introduction_1.mp4"},
        {"ID": 2, "VideoURL": video_url + "introduction_2.mp4"},
        {"ID": 3, "VideoURL": video_url + "/introduction_3.mp4"}
    ]
    return jsonify(videos)
