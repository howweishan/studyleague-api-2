from flask import Flask, jsonify
from flask_cors import CORS
from config import config
import os

# Import all route blueprints
from routes.users import users_bp
from routes.sessions import sessions_bp
from routes.rooms import rooms_bp
from routes.achievements import achievements_bp
from routes.discussions import discussions_bp
from routes.leaderboard import leaderboard_bp

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    
    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(discussions_bp)
    app.register_blueprint(leaderboard_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'StudyLeague API is running'
        }), 200
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to StudyLeague API',
            'version': '1.0.0',
            'endpoints': {
                'users': '/api/users',
                'sessions': '/api/sessions',
                'rooms': '/api/rooms',
                'achievements': '/api/achievements',
                'discussions': '/api/discussions',
                'leaderboard': '/api/leaderboard'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
