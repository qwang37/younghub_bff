from flask import Blueprint, render_template

video_bp = Blueprint('videos', __name__)

@video_bp.route('/videos')
def list_videos():
    return ["https://younghubstorage.blob.core.windows.net/short-video/introduction_1.mp4",
            "https://younghubstorage.blob.core.windows.net/short-video/introduction_2.mp4",
            "https://younghubstorage.blob.core.windows.net/short-video/introduction_3.mp4"]
