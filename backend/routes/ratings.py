"""
Rating routes for submitting and retrieving movie ratings
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db, Rating, Movie

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/api/rate', methods=['POST'])
def submit_rating():
    """Submit or update a movie rating"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'movie_id' not in data or 'rating' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: user_id, movie_id, rating'
            }), 400
        
        user_id = data['user_id']
        movie_id = data['movie_id']
        rating_value = data['rating']
        
        # Validate rating value (1-5 stars)
        if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
            return jsonify({
                'success': False,
                'error': 'Rating must be an integer between 1 and 5'
            }), 400
        
        db = get_db()
        
        # Get movie details
        movie = db.query(Movie).filter_by(id=movie_id).first()
        if not movie:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404
        
        # Check if rating already exists
        existing_rating = db.query(Rating).filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = rating_value
            existing_rating.timestamp = datetime.utcnow()
            message = 'Rating updated successfully'
        else:
            # Create new rating
            new_rating = Rating(
                user_id=user_id,
                movie_id=movie_id,
                movie_title=movie.title,
                rating=rating_value,
                timestamp=datetime.utcnow()
            )
            db.add(new_rating)
            message = 'Rating saved successfully'
        
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ratings_bp.route('/api/ratings/<user_id>', methods=['GET'])
def get_user_ratings(user_id):
    """Get all ratings for a user"""
    try:
        db = get_db()
        
        # Get all ratings for user
        ratings = db.query(Rating).filter_by(user_id=user_id).order_by(
            Rating.timestamp.desc()
        ).all()
        
        # Convert to dict
        ratings_list = [rating.to_dict() for rating in ratings]
        
        db.close()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'total_ratings': len(ratings_list),
            'ratings': ratings_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ratings_bp.route('/api/rating/<user_id>/<movie_id>', methods=['GET'])
def get_movie_rating(user_id, movie_id):
    """Get user's rating for a specific movie"""
    try:
        db = get_db()
        
        rating = db.query(Rating).filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()
        
        db.close()
        
        if not rating:
            return jsonify({
                'success': True,
                'rating': None
            }), 200
        
        return jsonify({
            'success': True,
            'rating': rating.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
