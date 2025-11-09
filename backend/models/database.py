"""
Database models for the Movie Recommendation System
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Movie(Base):
    """Movie model representing the movies in the database"""
    __tablename__ = 'movies'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    certificate = Column(String)
    runtime = Column(String)
    genres = Column(JSON)  # Store as list of genres
    imdb_rating = Column(Float)
    overview = Column(Text)
    meta_score = Column(Integer)
    director = Column(String)
    star1 = Column(String)
    star2 = Column(String)
    star3 = Column(String)
    star4 = Column(String)
    no_of_votes = Column(Integer)
    gross = Column(String)
    poster_link = Column(String)
    
    def to_dict(self):
        """Convert movie object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'certificate': self.certificate,
            'runtime': self.runtime,
            'genres': self.genres,
            'imdb_rating': self.imdb_rating,
            'overview': self.overview,
            'meta_score': self.meta_score,
            'director': self.director,
            'star1': self.star1,
            'star2': self.star2,
            'star3': self.star3,
            'star4': self.star4,
            'no_of_votes': self.no_of_votes,
            'gross': self.gross,
            'poster_link': self.poster_link
        }


class WatchHistory(Base):
    """Watch history model for tracking user watch events"""
    __tablename__ = 'watch_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    movie_id = Column(String, nullable=False)
    movie_metadata = Column(JSON)  # Store movie details at time of watch
    watch_timestamp = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=True)
    
    def to_dict(self):
        """Convert watch history object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'movie_metadata': self.movie_metadata,
            'watch_timestamp': self.watch_timestamp.isoformat() if self.watch_timestamp else None,
            'completed': self.completed
        }


class Rating(Base):
    """Rating model for storing user movie ratings"""
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    movie_id = Column(String, nullable=False)
    movie_title = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert rating object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'movie_title': self.movie_title,
            'rating': self.rating,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


# Database connection setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_wBLldE74pimx@ep-sweet-thunder-adgkv27e-pooler.c-2.us-east-1.aws.neon.tech/movie_recom?sslmode=require&channel_binding=require')

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e
