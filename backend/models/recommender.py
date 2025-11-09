"""
Movie Recommendation Algorithm
Enhanced Multi-Factor Content-Based Filtering
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_db, Movie, WatchHistory, Rating
from collections import defaultdict

class MovieRecommender:
    """
    Content-based recommendation system using:
    - Genre matching (40% weight)
    - Director matching (25% weight)
    - Actor matching (20% weight)
    - IMDB quality score (15% weight)
    """
    
    def __init__(self):
        self.db = get_db()
    
    def calculate_interaction_score(self, movie_id, user_id):
        """
        Calculate interaction score for a movie-user pair
        Returns: float between -0.5 and 1.0
        
        Interaction Weight Table:
        - Watched + Rated 5★: 1.0 (Loved it)
        - Watched + Rated 4★: 0.8 (Liked it)
        - Watched + Rated 3★: 0.5 (Okay)
        - Watched only: 0.5 (Interested)
        - Rated 5★ only: 0.6 (Knows & loves)
        - Watched + Rated 2★: -0.3 (Didn't like)
        - Watched + Rated 1★: -0.5 (Hated it)
        """
        # Check if watched
        watched = self.db.query(WatchHistory).filter_by(
            user_id=user_id, 
            movie_id=movie_id
        ).first()
        
        # Check rating
        rating_obj = self.db.query(Rating).filter_by(
            user_id=user_id,
            movie_id=movie_id
        ).first()
        
        rating = rating_obj.rating if rating_obj else None
        
        # Combined interactions (strongest signals)
        if watched and rating:
            if rating == 5:
                return 1.0      # Strongest positive
            elif rating == 4:
                return 0.8      # Strong positive
            elif rating == 3:
                return 0.5      # Neutral/mild positive
            elif rating == 2:
                return -0.3     # Mild negative (avoid)
            else:  # rating == 1
                return -0.5     # Strong negative (definitely avoid)
        
        # Implicit feedback only
        elif watched and not rating:
            return 0.5          # Moderate positive signal
        
        # Explicit feedback only
        elif rating and not watched:
            if rating >= 4:
                return 0.6      # Positive signal
            elif rating == 3:
                return 0.3      # Mild positive
            else:
                return -0.3     # Negative signal
        
        return 0  # No interaction
    
    def build_user_profile(self, user_id):
        """
        Build comprehensive user preference profile
        Returns: dict with weighted genre/director/actor preferences
        """
        # Get all watched movies
        watch_history = self.db.query(WatchHistory).filter_by(user_id=user_id).all()
        
        # Initialize weighted preferences
        genre_weights = defaultdict(float)
        director_weights = defaultdict(float)
        actor_weights = defaultdict(float)
        
        positive_interactions = 0
        total_interactions = 0
        
        # Process each watch event
        for watch in watch_history:
            movie_id = watch.movie_id
            interaction_score = self.calculate_interaction_score(movie_id, user_id)
            
            # Count all interactions (positive or negative)
            if interaction_score != 0:
                total_interactions += 1
            
            # Only consider positive interactions for building preferences
            if interaction_score > 0:
                positive_interactions += 1
                
                # Get movie metadata
                metadata = watch.movie_metadata
                
                # Weight genres
                if metadata and 'genres' in metadata:
                    for genre in metadata['genres']:
                        genre_weights[genre] += interaction_score
                
                # Weight director
                if metadata and 'director' in metadata:
                    director_weights[metadata['director']] += interaction_score
                
                # Weight actors
                if metadata and 'stars' in metadata:
                    for actor in metadata['stars']:
                        if actor:
                            actor_weights[actor] += interaction_score
        
        return {
            'genres': dict(genre_weights),
            'directors': dict(director_weights),
            'actors': dict(actor_weights),
            'total_positive_interactions': positive_interactions,
            'total_interactions': total_interactions
        }
    
    def score_candidate_movie(self, movie, user_profile):
        """
        Calculate recommendation score for a candidate movie
        Returns: dict with final_score and breakdown
        """
        # 1. GENRE MATCHING (40% weight)
        genre_score = 0
        total_genre_weight = sum(user_profile['genres'].values())
        
        if total_genre_weight > 0 and movie.genres:
            for genre in movie.genres:
                if genre in user_profile['genres']:
                    genre_score += user_profile['genres'][genre]
            genre_score = genre_score / total_genre_weight
        
        # 2. DIRECTOR MATCHING (25% weight)
        director_score = 0
        total_director_weight = sum(user_profile['directors'].values())
        
        if total_director_weight > 0 and movie.director in user_profile['directors']:
            director_score = user_profile['directors'][movie.director] / total_director_weight
        
        # 3. ACTOR MATCHING (20% weight)
        actor_score = 0
        total_actor_weight = sum(user_profile['actors'].values())
        
        if total_actor_weight > 0:
            movie_actors = [movie.star1, movie.star2, movie.star3, movie.star4]
            for actor in movie_actors:
                if actor and actor in user_profile['actors']:
                    actor_score += user_profile['actors'][actor]
            if actor_score > 0:
                actor_score = actor_score / (total_actor_weight * 4)
        
        # 4. QUALITY SCORE (15% weight)
        quality_score = (movie.imdb_rating / 10.0) if movie.imdb_rating else 0
        
        # FINAL WEIGHTED SCORE
        final_score = (
            genre_score * 0.40 +
            director_score * 0.25 +
            actor_score * 0.20 +
            quality_score * 0.15
        )
        
        return {
            'movie': movie,
            'final_score': final_score,
            'breakdown': {
                'genre_score': genre_score,
                'director_score': director_score,
                'actor_score': actor_score,
                'quality_score': quality_score
            }
        }
    
    def get_matching_genres(self, movie, genre_weights):
        """Get matching genres for explanation"""
        matching = []
        for genre in movie.genres:
            if genre in genre_weights and genre_weights[genre] > 0:
                matching.append(genre)
        return matching
    
    def get_matching_actors(self, movie, actor_weights):
        """Get matching actors for explanation"""
        matching = []
        movie_actors = [movie.star1, movie.star2, movie.star3, movie.star4]
        for actor in movie_actors:
            if actor and actor in actor_weights and actor_weights[actor] > 0:
                matching.append(actor)
        return matching
    
    def get_recommendations(self, user_id, num_recommendations=12):
        """
        Main recommendation function
        Returns: dict with recommendations and explanations
        """
        # Build user profile
        user_profile = self.build_user_profile(user_id)
        
        # Check minimum threshold - use total interactions (including negative ratings)
        if user_profile['total_interactions'] < 3:
            return {
                'success': False,
                'message': 'Watch or rate at least 3 movies to get recommendations',
                'current_count': user_profile['total_interactions'],
                'required_count': 3
            }
        
        # Check if we have any positive interactions to base recommendations on
        if user_profile['total_positive_interactions'] == 0:
            # User has only negative ratings - recommend popular/highly-rated movies
            all_movies = self.db.query(Movie).order_by(Movie.imdb_rating.desc()).limit(num_recommendations).all()
            watched_movies = self.db.query(WatchHistory).filter_by(user_id=user_id).all()
            watched_ids = {watch.movie_id for watch in watched_movies}
            
            recommendations = []
            for movie in all_movies:
                if movie.id not in watched_ids:
                    recommendations.append({
                        'movie': movie.to_dict(),
                        'score': movie.imdb_rating / 10.0 if movie.imdb_rating else 0,
                        'reasons': ['Popular & highly-rated movie']
                    })
                    if len(recommendations) >= num_recommendations:
                        break
            
            return {
                'success': True,
                'recommendations': recommendations,
                'based_on': {
                    'total_watched': len(watched_ids),
                    'total_rated': self.db.query(Rating).filter_by(user_id=user_id).count(),
                    'total_interactions': len(watched_ids)
                },
                'note': 'Showing popular movies. Rate some movies higher to get personalized recommendations!'
            }
        
        # Get all movies
        all_movies = self.db.query(Movie).all()
        
        # Get watched movie IDs
        watched_movies = self.db.query(WatchHistory).filter_by(user_id=user_id).all()
        watched_ids = {watch.movie_id for watch in watched_movies}
        
        # Filter to unwatched movies only
        candidate_movies = [m for m in all_movies if m.id not in watched_ids]
        
        if not candidate_movies:
            return {
                'success': False,
                'message': "You've watched all available movies! Check back for new additions.",
                'current_count': len(watched_ids),
                'required_count': 3
            }
        
        # Score each candidate
        scored_movies = []
        for movie in candidate_movies:
            result = self.score_candidate_movie(movie, user_profile)
            scored_movies.append(result)
        
        # Sort by score (descending), then by IMDB rating, then by year
        scored_movies.sort(
            key=lambda x: (x['final_score'], x['movie'].imdb_rating or 0, x['movie'].year or 0),
            reverse=True
        )
        
        # Generate recommendations with explanations
        recommendations = []
        for item in scored_movies[:num_recommendations]:
            movie = item['movie']
            breakdown = item['breakdown']
            
            # Build explanation based on highest contributing factors
            reasons = []
            
            if breakdown['genre_score'] > 0.3:
                top_genres = self.get_matching_genres(movie, user_profile['genres'])
                if top_genres:
                    genres_str = ', '.join(top_genres[:2])
                    reasons.append(f"You love {genres_str} movies")
            
            if breakdown['director_score'] > 0.3:
                reasons.append(f"You enjoyed other films by {movie.director}")
            
            if breakdown['actor_score'] > 0.2:
                top_actors = self.get_matching_actors(movie, user_profile['actors'])
                if top_actors:
                    reasons.append(f"Stars {top_actors[0]} from your favorites")
            
            if breakdown['quality_score'] > 0.8:
                reasons.append(f"Highly rated ({movie.imdb_rating}/10)")
            
            if not reasons:
                reasons.append('Based on your viewing history')
            
            recommendations.append({
                'movie': movie.to_dict(),
                'score': round(item['final_score'], 3),
                'reasons': reasons
            })
        
        # Get rating count
        rating_count = self.db.query(Rating).filter_by(user_id=user_id).count()
        
        return {
            'success': True,
            'recommendations': recommendations,
            'based_on': {
                'total_watched': len(watched_ids),
                'total_rated': rating_count,
                'total_interactions': len(watched_ids)
            }
        }
    
    def close(self):
        """Close database connection"""
        self.db.close()
