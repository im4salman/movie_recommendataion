"""
Main Flask Application for Movie Recommendation System
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import routes
from routes.movies import movies_bp
from routes.watch import watch_bp
from routes.ratings import ratings_bp
from routes.recommendations import recommendations_bp

# Import database
from models.database import init_db

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(movies_bp)
app.register_blueprint(watch_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(recommendations_bp)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Movie Recommendation API is running!',
        'version': '1.0.0'
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Movie Recommendation API',
        'endpoints': {
            'movies': '/api/movies',
            'watch': '/api/watch',
            'rate': '/api/rate',
            'recommendations': '/api/recommendations/<user_id>',
            'user_activity': '/api/user/<user_id>/activity'
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize database tables
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    # Run Flask app
    port = 5001
    print("\n🎬 Starting Movie Recommendation API...")
    print(f"📡 API running on: http://localhost:{port}")
    print("📚 Available endpoints:")
    print("   - GET  /api/movies")
    print("   - GET  /api/movies/<movie_id>")
    print("   - POST /api/watch")
    print("   - POST /api/rate")
    print("   - GET  /api/watch-history/<user_id>")
    print("   - GET  /api/ratings/<user_id>")
    print("   - GET  /api/recommendations/<user_id>")
    print("   - GET  /api/user/<user_id>/activity")
    print("\n✨ Ready to serve recommendations!\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
