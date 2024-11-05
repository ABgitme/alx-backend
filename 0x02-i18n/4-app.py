#!/usr/bin/env python3
"""To allow forcing a particular locale by
passing a locale parameter in the URL"""
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


def get_locale():
    """
    Determine the best match for the user's language preference.

    If a 'locale' parameter is provided in the URL
    and matches a supported language,it will be used
    as the language. Otherwise, fall back to the best match based
    on the browser's language preferences.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    # Check if 'locale' parameter is in the request and is a supported language
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
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
    Render the home page with translated content.

    Returns:
        Response: A rendered HTML template for the home page.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    """
    Run the Flask application on the local development server.
    """
    app.run(debug=True)
