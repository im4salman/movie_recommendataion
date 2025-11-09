"""
Movie routes for browsing and searching movies
"""
from flask import Blueprint, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db, Movie

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/api/movies', methods=['GET'])
def get_movies():
    """
    Get all movies with optional filtering
    Query params: search (title search), genre (filter by genre)
    """
    try:
        db = get_db()
        
        # Start with all movies
        query = db.query(Movie)
        
        # Apply search filter
        search_term = request.args.get('search', '').strip()
        if search_term:
            query = query.filter(Movie.title.ilike(f'%{search_term}%'))
        
        # Apply genre filter
        genre_filter = request.args.get('genre', '').strip()
        if genre_filter:
            # Filter movies that have this genre in their genres array
            query = query.filter(Movie.genres.contains([genre_filter]))
        
        # Execute query
        movies = query.all()
        
        # Convert to dict
        movies_dict = [movie.to_dict() for movie in movies]
        
        db.close()
        
        return jsonify({
            'success': True,
            'count': len(movies_dict),
            'movies': movies_dict
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@movies_bp.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    """Get single movie by ID"""
    try:
        db = get_db()
        movie = db.query(Movie).filter_by(id=movie_id).first()
        db.close()
        
        if not movie:
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404
        
        return jsonify({
            'success': True,
            'movie': movie.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@movies_bp.route('/api/genres', methods=['GET'])
def get_all_genres():
    """Get all unique genres from the database"""
    try:
        db = get_db()
        movies = db.query(Movie).all()
        
        # Collect all unique genres
        all_genres = set()
        for movie in movies:
            if movie.genres:
                all_genres.update(movie.genres)
        
        db.close()
        
        return jsonify({
            'success': True,
            'genres': sorted(list(all_genres))
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
