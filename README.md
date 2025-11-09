# Movie Recommendation System

A full-stack movie recommendation web application built with React and Python Flask that uses both watch history and ratings to generate personalized recommendations.

## 🎯 Project Overview

This system combines **implicit feedback** (what users watch) and **explicit feedback** (how users rate) for better recommendation accuracy - mimicking industry standards like Netflix and YouTube.

### Core Features

1. **Browse Movies** - Search and filter from 1000+ movies
2. **Watch Tracking** - Simulated watch experience with progress tracking
3. **Rating System** - Interactive 5-star rating for movies
4. **Personalized Recommendations** - AI-powered suggestions based on viewing history

## 🛠️ Technology Stack

### Frontend
- **React.js** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **CSS** - Styling (simple, clean, dark theme)

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Web framework
- **PostgreSQL** (Neon) - Database
- **SQLAlchemy** - ORM
- **Pandas** - Data manipulation

## 📁 Project Structure

```
MovieRecommendation/
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── models/
│   │   ├── database.py       # Database models
│   │   └── recommender.py    # Recommendation algorithm
│   ├── routes/               # API endpoints
│   │   ├── movies.py
│   │   ├── watch.py
│   │   ├── ratings.py
│   │   └── recommendations.py
│   └── utils/
│       └── data_loader.py    # CSV import script
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service
│   │   └── App.js           # Main app
│   └── package.json
│
├── imdb_top_1000.csv         # Movie dataset
└── README.md                 # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Internet connection (for cloud database)

### Complete Setup & Run Instructions

#### Step 1: Backend Setup

1. **Navigate to the project root directory:**
```bash
cd /path/to/MovieRecommendatiion
```

2. **Go to backend directory:**
```bash
cd backend
```

3. **Create a Python virtual environment:**
```bash
python3 -m venv venv
```

4. **Activate the virtual environment:**

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

5. **Install all Python dependencies:**
```bash
pip install -r requirements.txt
```

6. **Import movie data into database:**
```bash
python utils/data_loader.py
```

This will:
- Create all necessary database tables in PostgreSQL
- Import 1000 movies from `imdb_top_1000.csv`
- Show progress and import summary
- Take approximately 1-2 minutes

7. **Start the Flask backend server:**
```bash
python app.py
```

✅ Backend should now be running at: **http://localhost:5000**

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Keep this terminal window open!**

#### Step 2: Frontend Setup

1. **Open a NEW terminal window** (keep backend running)

2. **Navigate to the frontend directory:**
```bash
cd /path/to/MovieRecommendatiion/frontend
```

3. **Install Node.js dependencies:**
```bash
npm install
```

This will install React and all required packages (takes 1-2 minutes).

4. **Start the React development server:**
```bash
npm start
```

✅ Frontend will automatically open in your browser at: **http://localhost:3000**

If it doesn't open automatically, manually visit: **http://localhost:3000**

**Keep this terminal window open too!**

### Verification

You should now have:
- ✅ Backend running on http://localhost:5000
- ✅ Frontend running on http://localhost:3000
- ✅ Browser showing the Movie Recommendation app

#### Quick Test

1. You'll see a login page - enter any user ID (e.g., "user123")
2. Click "Browse Movies" to see the movie catalog
3. Search for a movie or browse the list
4. Click "Watch" on any movie to simulate watching
5. Rate the movie when prompted
6. After watching/rating 3+ movies, go to "Recommendations" to see personalized suggestions

### Stopping the Application

To stop the servers:
1. Go to each terminal window
2. Press `Ctrl + C` (or `Cmd + C` on Mac)
3. Deactivate the Python virtual environment: `deactivate`

## 🎬 Using the Application

### 1. Browse Movies
- Search by title using the search bar
- Filter by multiple genres
- View movie details on hover
- See IMDB ratings and genres

### 2. Watch Movies
- Click "▶ Watch" button on any movie
- Watch simulation modal appears with:
  - Movie poster
  - Progress bar
  - Play/Pause controls
- Mark as completed when done
- Rating prompt appears automatically

### 3. Rate Movies
- Rate anytime using the star rating widget
- 1-5 stars (1 = didn't like, 5 = loved it)
- Update existing ratings
- Ratings improve recommendations

### 4. Get Recommendations
- Navigate to "Recommendations" page
- View your activity summary
- See your watch history
- Get personalized recommendations with explanations
- **Minimum 3 interactions required** (watches or ratings)

## 🧠 Recommendation Algorithm

### Algorithm: Enhanced Multi-Factor Content-Based Filtering

#### Scoring Components
1. **Genre Matching** - 40% weight
2. **Director Matching** - 25% weight
3. **Actor Matching** - 20% weight
4. **IMDB Quality Score** - 15% weight

#### Interaction Weights
| Interaction | Weight | Meaning |
|------------|--------|---------|
| Watched + Rated 5★ | 1.0 | Loved it! |
| Watched + Rated 4★ | 0.8 | Really liked it |
| Watched + Rated 3★ | 0.5 | It was okay |
| Watched only | 0.5 | Interested |
| Rated 5★ only | 0.6 | Knows & loves |
| Watched + Rated 2★ | -0.3 | Didn't like |
| Watched + Rated 1★ | -0.5 | Hated it |

#### How It Works

1. **Build User Profile**
   - Analyze watch history and ratings
   - Extract genre preferences
   - Identify favorite directors
   - Track preferred actors
   - Weight by interaction strength

2. **Score Candidate Movies**
   - Match genres with user preferences
   - Match directors with favorites
   - Match actors with preferred stars
   - Factor in IMDB quality score
   - Calculate weighted final score

3. **Generate Recommendations**
   - Sort by final score (highest first)
   - Exclude already watched movies
   - Return top 12 recommendations
   - Provide explanation for each

4. **Explain Recommendations**
   - "You love Sci-Fi, Thriller movies"
   - "You enjoyed other films by Christopher Nolan"
   - "Stars Leonardo DiCaprio from your favorites"
   - "Highly rated (8.8/10)"

### Example Calculation

If you watch and rate 5★ for:
- Inception (Sci-Fi, Thriller by Christopher Nolan)
- The Dark Knight (Action, Crime by Christopher Nolan)
- Interstellar (Sci-Fi, Drama by Christopher Nolan)

You'll get recommendations like:
- **Tenet** (Sci-Fi, Thriller by Christopher Nolan)
  - "You love Sci-Fi, Thriller movies"
  - "You enjoyed other films by Christopher Nolan"
- **The Matrix** (Sci-Fi, Action)
  - "You love Sci-Fi movies"
  - "Highly rated (8.7/10)"

## 📊 API Endpoints

### Movies
- `GET /api/movies` - Get all movies (with search/filter)
- `GET /api/movies/<id>` - Get single movie
- `GET /api/genres` - Get all genres

### Watch Tracking
- `POST /api/watch` - Record watch event
- `GET /api/watch-history/<user_id>` - Get watch history

### Ratings
- `POST /api/rate` - Submit/update rating
- `GET /api/ratings/<user_id>` - Get all ratings
- `GET /api/rating/<user_id>/<movie_id>` - Get specific rating

### Recommendations
- `GET /api/recommendations/<user_id>` - Get recommendations
- `GET /api/user/<user_id>/activity` - Get user activity summary

## 🗄️ Database Schema

### Movies Table
```sql
id (String, Primary Key)
title, year, certificate, runtime
genres (JSON array)
imdb_rating, meta_score, overview
director, star1, star2, star3, star4
no_of_votes, gross, poster_link
```

### Watch History Table
```sql
id (Integer, Primary Key)
user_id, movie_id
movie_metadata (JSON)
watch_timestamp, completed
```

### Ratings Table
```sql
id (Integer, Primary Key)
user_id, movie_id, movie_title
rating (1-5), timestamp
```

## 🧪 Testing

### Test the Backend
```bash
# Health check
curl http://localhost:5000/api/health

# Get all movies
curl http://localhost:5000/api/movies

# Record a watch
curl -X POST http://localhost:5000/api/watch \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","movie_id":"inception_2010","completed":true}'

# Get recommendations
curl http://localhost:5000/api/recommendations/user123
```

### Test the Frontend
1. Open http://localhost:3000
2. Search for "Dark Knight"
3. Watch 3 different movies
4. Rate them (vary between 3-5 stars)
5. Go to Recommendations page
6. Verify personalized suggestions appear

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error:**
- Check DATABASE_URL in `.env` file
- Verify internet connection (Neon is cloud-hosted)
- Ensure PostgreSQL drivers installed

**Import Error:**
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**Port 5000 in use:**
- Change port in `app.py`: `app.run(port=5001)`
- Update frontend API_BASE_URL in `services/api.js`

### Frontend Issues

**Cannot connect to backend:**
- Verify backend is running on http://localhost:5000
- Check browser console for CORS errors
- Test backend endpoint directly with curl

**Movies not loading:**
- Check backend database has movie data
- Run `python utils/data_loader.py` to import

**Recommendations not showing:**
- User needs at least 3 interactions
- Check backend logs for algorithm errors
- Verify watch/rating data is being saved

## 📝 Notes

- **User ID:** Fixed as "user123" (no authentication)
- **Watch Feature:** Simulated (no real video playback)
- **Database:** PostgreSQL hosted on Neon (cloud)
- **CORS:** Enabled for all origins (development mode)
- **Debug Mode:** Enabled (disable in production)

## 🎓 College Project Guidelines

This project demonstrates:
- ✅ Full-stack web development (Frontend + Backend)
- ✅ RESTful API design
- ✅ Database integration (PostgreSQL)
- ✅ Content-based filtering algorithm
- ✅ User interaction tracking
- ✅ Data visualization (charts, statistics)
- ✅ Responsive design
- ✅ Error handling
- ✅ Code organization and documentation

## 🚧 Future Enhancements

- [ ] User authentication and profiles
- [ ] Collaborative filtering (user-user similarity)
- [ ] Machine learning model integration
- [ ] Real video streaming
- [ ] Social features (reviews, sharing)
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Movie detail page with cast/crew info

## 📄 License

This is a college project for educational purposes.

## 👥 Contributors

Built as a college project by:
- **Salman Hussain**

## 🙏 Acknowledgments

- IMDB for movie dataset
- Neon for PostgreSQL hosting
- Create React App for frontend setup
- Flask documentation
- React Router documentation

---

**Enjoy the movie recommendations! 🎬🍿**

For questions or issues, check the backend and frontend README files for detailed documentation.
