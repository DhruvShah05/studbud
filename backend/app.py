"""
Main Flask application
NotebookLM Clone Backend
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import os

# Import blueprints
from routes.workspace_routes import workspace_bp
from routes.source_routes import source_bp
from routes.studio_routes import studio_bp
from routes.auth_routes import auth_bp

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# TEMPORARY: Disable CORS entirely for testing
# WARNING: This allows ALL origins - NOT secure for production!
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Create upload folder if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Register blueprints
app.register_blueprint(workspace_bp, url_prefix='/api/workspace')
app.register_blueprint(source_bp, url_prefix='/api/sources')
app.register_blueprint(studio_bp, url_prefix='/api/studio')
app.register_blueprint(auth_bp, url_prefix='/api/auth')


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "NotebookLM Clone API",
        "version": "1.0.0"
    })


@app.route('/api/health')
def health():
    """Detailed health check"""
    from utils.s3_client import check_s3_connection
    
    return jsonify({
        "status": "healthy",
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "database_configured": bool(Config.DB_HOST and Config.DB_PASSWORD),
        "s3_configured": bool(Config.AWS_ACCESS_KEY_ID and Config.S3_BUCKET_NAME),
        "s3_connection": check_s3_connection()
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Only for local development - production uses gunicorn
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
