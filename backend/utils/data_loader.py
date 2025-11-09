"""
Data loader script to import CSV data into PostgreSQL database
"""
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_db, get_db, Movie

def clean_movie_id(title, year):
    """Generate a clean movie ID from title and year"""
    # Remove special characters and spaces, convert to lowercase
    clean_title = ''.join(e.lower() for e in title if e.isalnum() or e.isspace())
    clean_title = '_'.join(clean_title.split())
    return f"{clean_title}_{year}"

def parse_genres(genre_string):
    """Parse comma-separated genres into a list"""
    if pd.isna(genre_string):
        return []
    return [g.strip() for g in genre_string.split(',')]

def clean_numeric(value):
    """Clean numeric values from strings"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        # Remove commas and quotes
        value = value.replace(',', '').replace('"', '')
        try:
            return int(value)
        except:
            return None
    return int(value)

def import_movies_from_csv(csv_path):
    """Import movies from CSV file into the database"""
    
    # Initialize database
    print("Initializing database...")
    init_db()
    
    # Read CSV
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"Found {len(df)} movies in CSV")
    
    # Get database session
    db = get_db()
    
    # Counter for successful imports
    success_count = 0
    skip_count = 0
    
    # Import each movie
    for index, row in df.iterrows():
        try:
            # Skip if year is invalid
            year = row['Released_Year']
            if pd.isna(year) or year == 'PG':
                skip_count += 1
                continue
                
            year = int(year)
            
            # Generate movie ID
            movie_id = clean_movie_id(row['Series_Title'], year)
            
            # Check if movie already exists
            existing_movie = db.query(Movie).filter_by(id=movie_id).first()
            if existing_movie:
                print(f"Skipping duplicate: {row['Series_Title']} ({year})")
                skip_count += 1
                continue
            
            # Create movie object
            movie = Movie(
                id=movie_id,
                title=row['Series_Title'],
                year=year,
                certificate=row['Certificate'] if not pd.isna(row['Certificate']) else None,
                runtime=row['Runtime'] if not pd.isna(row['Runtime']) else None,
                genres=parse_genres(row['Genre']),
                imdb_rating=float(row['IMDB_Rating']) if not pd.isna(row['IMDB_Rating']) else None,
                overview=row['Overview'] if not pd.isna(row['Overview']) else None,
                meta_score=clean_numeric(row['Meta_score']),
                director=row['Director'] if not pd.isna(row['Director']) else None,
                star1=row['Star1'] if not pd.isna(row['Star1']) else None,
                star2=row['Star2'] if not pd.isna(row['Star2']) else None,
                star3=row['Star3'] if not pd.isna(row['Star3']) else None,
                star4=row['Star4'] if not pd.isna(row['Star4']) else None,
                no_of_votes=clean_numeric(row['No_of_Votes']),
                gross=row['Gross'] if not pd.isna(row['Gross']) else None,
                poster_link=row['Poster_Link'] if not pd.isna(row['Poster_Link']) else None
            )
            
            # Add to database
            db.add(movie)
            success_count += 1
            
            if success_count % 50 == 0:
                print(f"Imported {success_count} movies...")
                db.commit()
                
        except Exception as e:
            print(f"Error importing movie {row['Series_Title']}: {str(e)}")
            skip_count += 1
            continue
    
    # Commit remaining changes
    db.commit()
    db.close()
    
    print(f"\n✅ Import complete!")
    print(f"   Successfully imported: {success_count} movies")
    print(f"   Skipped: {skip_count} movies")
    
    return success_count

if __name__ == "__main__":
    # Path to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'imdb_top_1000.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        sys.exit(1)
    
    import_movies_from_csv(csv_path)
