"""
Recommendations routes for generating personalized movie recommendations
"""
from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.recommender import MovieRecommender
from models.database import get_db, WatchHistory, Rating

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized movie recommendations for a user"""
    try:
        # Get number of recommendations (default 12)
        num_recs = request.args.get('limit', 12, type=int)
        
        # Create recommender instance
        recommender = MovieRecommender()
        
        # Get recommendations
        result = recommender.get_recommendations(user_id, num_recommendations=num_recs)
        
        # Close recommender
        recommender.close()
        
        # Return result
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/api/user/<user_id>/activity', methods=['GET'])
def get_user_activity(user_id):
    """Get user activity summary"""
    try:
        db = get_db()
        
        # Get watch history
        watches = db.query(WatchHistory).filter_by(user_id=user_id).all()
        watched_count = len(watches)
        
        # Get ratings
        ratings = db.query(Rating).filter_by(user_id=user_id).all()
        rated_count = len(ratings)
        
        # Get recent activity
        recent_activity = []
        
        # Add recent watches
        recent_watches = db.query(WatchHistory).filter_by(user_id=user_id).order_by(
            WatchHistory.watch_timestamp.desc()
        ).limit(5).all()
        
        for watch in recent_watches:
            recent_activity.append({
                'type': 'watch',
                'movie_title': watch.movie_metadata.get('title', 'Unknown'),
                'timestamp': watch.watch_timestamp.isoformat() if watch.watch_timestamp else None
            })
        
        # Add recent ratings
        recent_ratings = db.query(Rating).filter_by(user_id=user_id).order_by(
            Rating.timestamp.desc()
        ).limit(5).all()
        
        for rating in recent_ratings:
            recent_activity.append({
                'type': 'rating',
                'movie_title': rating.movie_title,
                'rating': rating.rating,
                'timestamp': rating.timestamp.isoformat() if rating.timestamp else None
            })
        
        # Sort by timestamp
        recent_activity.sort(key=lambda x: x['timestamp'] if x['timestamp'] else '', reverse=True)
        recent_activity = recent_activity[:10]  # Keep top 10
        
        # Get top genres
        genre_counts = {}
        for watch in watches:
            if watch.movie_metadata and 'genres' in watch.movie_metadata:
                for genre in watch.movie_metadata['genres']:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_genres = [genre for genre, count in top_genres]
        
        # Get favorite directors
        director_counts = {}
        for watch in watches:
            if watch.movie_metadata and 'director' in watch.movie_metadata:
                director = watch.movie_metadata['director']
                if director:
                    director_counts[director] = director_counts.get(director, 0) + 1
        
        favorite_directors = sorted(director_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_directors = [director for director, count in favorite_directors]
        
        db.close()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'stats': {
                'movies_watched': watched_count,
                'movies_rated': rated_count,
                'can_get_recommendations': watched_count >= 3 or rated_count >= 3
            },
            'recent_activity': recent_activity,
            'top_genres': top_genres,
            'favorite_directors': favorite_directors
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
