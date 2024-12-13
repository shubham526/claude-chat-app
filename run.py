from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import logging
from app import create_app
from flask_talisman import Talisman
from flask_session import Session

# Load environment variables
load_dotenv()

# Create Flask application instance
app = create_app()

# Initialize Flask-Session
Session(app)

# Initialize Talisman for security headers
Talisman(app,
         content_security_policy={
             'default-src': "'self'",
             'script-src': [
                 "'self'",
                 "'unsafe-inline'",
                 'cdnjs.cloudflare.com',
                 'cdn.jsdelivr.net'
             ],
             'style-src': [
                 "'self'",
                 "'unsafe-inline'",
                 'cdn.jsdelivr.net',
                 'cdnjs.cloudflare.com'
             ],
             'font-src': [
                 "'self'",
                 'cdnjs.cloudflare.com'
             ],
             'img-src': ["'self'", 'data:'],
             'connect-src': ["'self'"]
         },
         force_https=False
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f'Unhandled Exception: {error}')
    return jsonify({"error": "An unexpected error occurred"}), 500


# Development settings
if __name__ == "__main__":
    # Check if running in development mode
    debug_mode = os.getenv('FLASK_ENV') == 'development'

    # Get host and port from environment variables or use defaults
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))


    # Additional security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Allow CORS for development
        if debug_mode:
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return response


    # Development-specific middleware
    if debug_mode:
        @app.before_request
        def log_request_info():
            app.logger.debug('Headers: %s', request.headers)
            app.logger.debug('Body: %s', request.get_data())

    # Start the application
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=debug_mode,
        ssl_context='adhoc' if not debug_mode else None  # Enable HTTPS in production
    )
