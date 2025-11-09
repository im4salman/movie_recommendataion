"""
Watch tracking routes for recording user watch events
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db, WatchHistory, Movie

watch_bp = Blueprint('watch', __name__)

@watch_bp.route('/api/watch', methods=['POST'])
def record_watch():
    """Record a watch event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'movie_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: user_id, movie_id'
            }), 400
        
        user_id = data['user_id']
        movie_id = data['movie_id']
        completed = data.get('completed', True)
        
        # Get movie metadata
        db = get_db()
        movie = db.query(Movie).filter_by(id=movie_id).first()
        
        if not movie:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404
        
        # Check if already watched
        existing_watch = db.query(WatchHistory).filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()
        
        if existing_watch:
            db.close()
            return jsonify({
                'success': True,
                'message': 'Watch already recorded',
                'prompt_rating': True
            }), 200
        
        # Prepare movie metadata
        movie_metadata = {
            'title': movie.title,
            'genres': movie.genres,
            'director': movie.director,
            'stars': [movie.star1, movie.star2, movie.star3, movie.star4],
            'imdb_rating': movie.imdb_rating,
            'year': movie.year
        }
        
        # Create watch history entry
        watch = WatchHistory(
            user_id=user_id,
            movie_id=movie_id,
            movie_metadata=movie_metadata,
            completed=completed,
            watch_timestamp=datetime.utcnow()
        )
        
        db.add(watch)
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Watch recorded successfully',
            'prompt_rating': True
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@watch_bp.route('/api/watch-history/<user_id>', methods=['GET'])
def get_watch_history(user_id):
    """Get user's watch history"""
    try:
        db = get_db()
        
        # Get all watch history for user
        watches = db.query(WatchHistory).filter_by(user_id=user_id).order_by(
            WatchHistory.watch_timestamp.desc()
        ).all()
        
        # Convert to dict
        watch_list = []
        for watch in watches:
            # Get current movie data
            movie = db.query(Movie).filter_by(id=watch.movie_id).first()
            if movie:
                watch_dict = watch.to_dict()
                watch_dict['current_movie_data'] = movie.to_dict()
                watch_list.append(watch_dict)
        
        db.close()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'total_watched': len(watch_list),
            'movies': watch_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
