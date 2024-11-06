#!/usr/bin/env python3
""" implement a user login simulation
and update HTML template to display appropriate messages"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


class Config:
    """Configuration class for setting up available languages,
    default locale, and timezone."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask app
app = Flask(__name__, template_folder='templates')
# Configure the app using the Config class
app.config.from_object(Config)

# Initialize Babel
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Retrieve a user based on the 'login_as' parameter from the URL.

    Returns:
        dict or None: The user dictionary if found, otherwise None.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """
    Set the user to a global variable on each request if the user is found.
    """
    g.user = get_user()


def get_locale() -> str:
    """
    Determine the best match for the user's language preference.

    If a 'locale' parameter is provided in the URL
    and matches a supported language,it will be used
    as the language. Otherwise, fall back to the best match based
    on the browser's language preferences.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    # 1. Check if a locale is explicitly provided in the URL parameters
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale

    # 2. If the user is logged in, check their preferred locale
    user_locale = g.user.get('locale') if g.user else None
    if user_locale in app.config["LANGUAGES"]:
        return user_locale
    # Default to best match based on browser settings
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Initialize Babel with the app and the locale selector function
babel.init_app(app, locale_selector=get_locale)


# Expose the get_locale function to the template context
@app.context_processor
def inject_locale():
    """Inject the get_locale function into the template context."""
    return {'get_locale': get_locale}


@app.route('/')
def home():
    """
    Render the home page with translated content and user information.

    Returns:
        Response: A rendered HTML template for the home page.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    """
    Run the Flask application on the local development server.
    """
    app.run(debug=True)
