import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Ensure backend directory is in the import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from src.routes.v1 import auth_bp, resume_bp, interview_bp, ats_bp, analytics_bp, settings_bp
from src.database.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS dynamically for production or local development
    frontend_url = os.environ.get('FRONTEND_URL', '*')
    CORS(app, resources={r"/api/*": {"origins": frontend_url}})
    
    # Initialize Database
    init_db(app)
    
    # Ensure upload folder is created
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints with versioned prefix (v1), overriding blueprint name to avoid collision
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth', name='auth_v1')
    app.register_blueprint(resume_bp, url_prefix='/api/v1/resume', name='resume_v1')
    app.register_blueprint(interview_bp, url_prefix='/api/v1/interview', name='interview_v1')
    app.register_blueprint(ats_bp, url_prefix='/api/v1/ats', name='ats_v1')
    app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics', name='analytics_v1')
    app.register_blueprint(settings_bp, url_prefix='/api/v1/settings', name='settings_v1')
    
    # Register blueprints at root for backwards compatibility
    app.register_blueprint(resume_bp, url_prefix='')
    app.register_blueprint(interview_bp, url_prefix='')
    app.register_blueprint(ats_bp, url_prefix='')    
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "AI Interview Preparation System API is running",
            "version": "v1"
        })
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
