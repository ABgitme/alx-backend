#!/usr/bin/env python3
"""set up and configure Flask-Babel with translations
for a multilingual Flask application"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


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


@babel.localeselector
def get_locale():
    """
    Determine the best match between the user's
    language preferences and supported languages.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """
    Render the home page with translated content.

    Returns:
        Response: A rendered HTML template for the home page.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    """
    Run the Flask application on the local development server.
    """
    app.run(debug=True)
