# Quick Start Guide - Movie Recommendation System

## ⚡ Fast Setup (5 minutes)

### Step 1: Setup Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Import movie data
python utils/data_loader.py

# Start backend server
python app.py
```

✅ Backend should be running at: **http://localhost:5000**

---

### Step 2: Setup Frontend (Terminal 2)

```bash
# Open a new terminal
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

✅ Frontend should open automatically at: **http://localhost:3000**

---

## 🎬 Quick Test

1. **Browse Movies**
   - Search for "Dark Knight"
   - Filter by "Action" genre
   - See the movie cards

2. **Watch a Movie**
   - Click "▶ Watch" on any movie
   - Wait for progress bar to reach 100%
   - Click "Mark as Completed"
   - Rate the movie (try 5 stars)

3. **Repeat for 2 More Movies**
   - Watch and rate at least 3 movies total
   - Vary the genres and ratings

4. **Get Recommendations**
   - Click "Recommendations" in navigation
   - See your activity summary
   - View personalized recommendations
   - Read the explanations

---

## 🚨 Common Issues

### Backend won't start
```bash
# Check Python version (needs 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt

# Check database connection
python -c "from models.database import init_db; init_db()"
```

### Frontend won't start
```bash
# Check Node version
node --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Can't connect to backend
```bash
# Test backend directly
curl http://localhost:5000/api/health

# If it fails, check if backend is running
# Make sure you see "Running on http://0.0.0.0:5000" in terminal
```

### No movies showing
```bash
# Reimport data
cd backend
python utils/data_loader.py

# Restart backend
python app.py
```

---

## 📊 Project Structure Overview

```
MovieRecommendation/
├── backend/           # Python Flask API
│   ├── app.py        # Main server file
│   ├── models/       # Database & algorithm
│   └── routes/       # API endpoints
│
├── frontend/         # React UI
│   └── src/
│       ├── components/  # UI components
│       ├── pages/      # Pages
│       └── services/   # API calls
│
└── imdb_top_1000.csv  # Movie data
```

---

## 🎯 What Each Part Does

### Backend (Python Flask)
- Stores movies in PostgreSQL database
- Tracks what you watch and rate
- Calculates personalized recommendations
- Provides API endpoints for frontend

### Frontend (React)
- Shows movie browsing interface
- Handles watch simulation
- Collects ratings
- Displays recommendations

### Database (PostgreSQL on Neon)
- Stores 1000 movies
- Tracks your watch history
- Stores your ratings
- Cloud-hosted (no local setup needed)

---

## 💡 Tips

1. **Keep both terminals open** - Backend and frontend must run simultaneously
2. **Virtual environment must be activated** - You'll see `(venv)` in terminal
3. **Wait for data import** - First time setup takes ~2-3 minutes
4. **Try different genres** - Watch variety of movies for better recommendations
5. **Rate honestly** - Algorithm learns from your ratings (1-5 stars)

---

## 📞 Help

If you encounter issues:

1. Check both terminals for error messages
2. Read the error message carefully
3. Check main README.md for detailed troubleshooting
4. Verify Python and Node versions
5. Make sure internet connection is active (database is cloud-hosted)

---

## ✨ Next Steps

After successful setup:

1. Explore the code in your IDE
2. Read the algorithm explanation in main README
3. Test different scenarios
4. Modify CSS to customize appearance
5. Add your own features

---

**Happy coding! 🚀**
