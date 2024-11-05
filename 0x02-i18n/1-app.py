#!/usr/bin/env python3
"""integrate Babel with Flask for managing multilingual support"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """
    Configuration class for setting up available languages,
    default locale, and timezone.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask app
app = Flask(__name__, template_folder='templates')
# Configure the app using the Config class
app.config.from_object(Config)

# Initialize Babel with the app
babel = Babel(app)


@app.route('/', strict_slashes=False)
def home():
    """
    Render the home page with a simple greeting.

    Returns:
        Response: A rendered HTML template for the home page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    """
    Run the Flask application on the local development server.
    """
    app.run(debug=True)
