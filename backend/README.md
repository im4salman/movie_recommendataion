# Movie Recommendation System - Backend

This is the Python Flask backend for the Movie Recommendation System.

## Technology Stack

- **Python 3.8+**
- **Flask** - Web framework
- **PostgreSQL** - Database (Neon)
- **SQLAlchemy** - ORM
- **Flask-CORS** - Cross-origin requests
- **Pandas** - Data manipulation

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── models/
│   ├── database.py            # Database models and connection
│   └── recommender.py         # Recommendation algorithm
├── routes/
│   ├── movies.py              # Movie endpoints
│   ├── watch.py               # Watch tracking endpoints
│   ├── ratings.py             # Rating endpoints
│   └── recommendations.py     # Recommendation endpoints
└── utils/
    └── data_loader.py         # CSV import script
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database and Import Data

```bash
# Import movies from CSV to PostgreSQL
python utils/data_loader.py
```

This will:
- Create all database tables
- Import movies from `imdb_top_1000.csv`
- Show progress and summary

### 5. Run the Application

```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Movies

- **GET /api/movies** - Get all movies
  - Query params: `search` (title search), `genre` (filter by genre)
  
- **GET /api/movies/<movie_id>** - Get single movie by ID

- **GET /api/genres** - Get all unique genres

### Watch Tracking

- **POST /api/watch** - Record watch event
  ```json
  {
    "user_id": "user123",
    "movie_id": "inception_2010",
    "completed": true
  }
  ```

- **GET /api/watch-history/<user_id>** - Get user's watch history

### Ratings

- **POST /api/rate** - Submit or update rating
  ```json
  {
    "user_id": "user123",
    "movie_id": "inception_2010",
    "rating": 5
  }
  ```

- **GET /api/ratings/<user_id>** - Get all user ratings

- **GET /api/rating/<user_id>/<movie_id>** - Get specific movie rating

### Recommendations

- **GET /api/recommendations/<user_id>** - Get personalized recommendations
  - Query params: `limit` (number of recommendations, default 12)

- **GET /api/user/<user_id>/activity** - Get user activity summary

### Health Check

- **GET /api/health** - Check if API is running

## Recommendation Algorithm

The system uses **Enhanced Multi-Factor Content-Based Filtering** with:

### Scoring Components
1. **Genre Matching** - 40% weight
2. **Director Matching** - 25% weight
3. **Actor Matching** - 20% weight
4. **IMDB Quality Score** - 15% weight

### Interaction Weights
- Watched + Rated 5★: 1.0 (Loved it)
- Watched + Rated 4★: 0.8 (Liked it)
- Watched + Rated 3★: 0.5 (Okay)
- Watched only: 0.5 (Interested)
- Rated 5★ only: 0.6 (Knows & loves)
- Watched + Rated 2★: -0.3 (Didn't like)
- Watched + Rated 1★: -0.5 (Hated it)

### Minimum Requirements
- User must have at least 3 positive interactions (watches or ratings ≥3★)
- Already watched movies are excluded from recommendations

## Testing

Use Postman, curl, or any HTTP client to test the endpoints.

Example:
```bash
# Get all movies
curl http://localhost:5000/api/movies

# Record a watch
curl -X POST http://localhost:5000/api/watch \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","movie_id":"the_shawshank_redemption_1994","completed":true}'

# Get recommendations
curl http://localhost:5000/api/recommendations/user123
```

## Database Schema

### Movies Table
- id (String, Primary Key)
- title, year, certificate, runtime
- genres (JSON array)
- imdb_rating, meta_score
- overview, director
- star1, star2, star3, star4
- no_of_votes, gross
- poster_link

### Watch History Table
- id (Integer, Primary Key)
- user_id, movie_id
- movie_metadata (JSON)
- watch_timestamp
- completed (Boolean)

### Ratings Table
- id (Integer, Primary Key)
- user_id, movie_id, movie_title
- rating (1-5)
- timestamp

## Troubleshooting

### Database Connection Error
- Verify the DATABASE_URL in `.env` file
- Check internet connection (Neon is cloud-hosted)
- Ensure PostgreSQL extension is installed

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

## Development

To add new features:
1. Create new route in `routes/` folder
2. Register blueprint in `app.py`
3. Update this README with new endpoints
4. Test thoroughly

## Notes

- Default user_id is "user123" (hardcoded in frontend)
- Database is hosted on Neon (PostgreSQL cloud)
- CORS is enabled for all origins (development mode)
- Debug mode is enabled (disable in production)
