# 1. Import necessary libraries
from flask import Flask, jsonify
from markupsafe import escape

# Context provided (can be updated dynamically in a real app)
CURRENT_TIME = "Monday, April 21, 2025 at 11:46:30 AM CEST"
CURRENT_LOCATION = "Milan, Lombardy, Italy"

# 2. Create a Flask application instance
#    __name__ helps Flask locate templates and static files
app = Flask(__name__)

# 3. Define routes and their corresponding view functions

# Route for the homepage '/'
@app.route('/')
def home():
    """Serves the homepage."""
    # Simple HTML response
    html_content = f"""
    <h1>Welcome to the Flask Server!</h1>
    <p>This is the homepage.</p>
    <p>Current context:</p>
    <ul>
        <li>Time: {CURRENT_TIME}</li>
        <li>Location: {CURRENT_LOCATION}</li>
    </ul>
    <p>Try visiting <a href="/about">/about</a> or <a href="/user/YourName">/user/YourName</a> or <a href="/api/data">/api/data</a>.</p>
    """
    return html_content

# Route for the '/about' page
@app.route('/about')
def about():
    """Serves the about page."""
    return "<h1>About Page</h1><p>This is a simple Flask server example.</p>"

# Dynamic route that accepts a username parameter
# The <username> part in the URL is captured as a variable
@app.route('/user/<username>')
def show_user_profile(username):
    """Shows a user profile page."""
    # escape() is used to prevent injection attacks if displaying user input
    safe_username = escape(username)
    return f"<h1>Hello, {safe_username}!</h1><p>Welcome to your user page.</p>"

# Route for serving JSON data
@app.route('/api/data')
def get_data():
    """Serves some sample JSON data."""
    data = {
        'message': 'This is some JSON data from the server.',
        'items': ['item1', 'item2', 'item3'],
        'status': 'success',
        'context_time': CURRENT_TIME,
        'context_location': CURRENT_LOCATION
    }
    # jsonify() converts the Python dictionary to a JSON response
    return jsonify(data)

# 4. Run the Flask development server
if __name__ == '__main__':
    # debug=True enables auto-reloading when code changes
    # and provides detailed error pages.
    # IMPORTANT: Do NOT run with debug=True in a production environment!
    app.run(debug=True)
    # You can specify host and port: app.run(host='0.0.0.0', port=8000)
    # host='0.0.0.0' makes it accessible from other devices on your network.