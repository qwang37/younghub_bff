from flask import render_template, request, redirect, url_for, flash
from app import app

# Define the root route
@app.route('/')
def home():
    return render_template('index.html')  # Renders the home page

# Define a route for error handling (e.g., 404 page)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
