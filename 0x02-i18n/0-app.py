#!/usr/bin/env python3
"""Create an instance of the Flask
class for the web application"""
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/', strict_slashes=False)
def home():
    """
    Render the home page with a simple greeting.

    Returns:
        Response: A rendered HTML template for the home page.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    """
    Run the Flask application on the local development server.
    """
    app.run(debug=True)
