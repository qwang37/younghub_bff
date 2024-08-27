from flask import render_template, request, redirect, url_for, flash
from app import app

# Define the root route
@app.route('/')
def home():
    return render_template('index.html')  # Renders the home page

# Define a dynamic route with a parameter
@app.route('/hello/<name>')
def hello(name):
    return f"Hello, {name}!"  # Returns a greeting with the provided name

# Define a route that handles both GET and POST methods
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')  # Retrieve form data
        flash(f'Form submitted successfully! Name: {name}', 'success')
        return redirect(url_for('home'))
    return render_template('submit.html')  # Renders the form submission page

# Define a route with query parameters
@app.route('/search')
def search():
    query = request.args.get('query', '')  # Retrieve query parameter
    return f"Search results for: {query}"  # Display the search query

# Define a route for error handling (e.g., 404 page)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
