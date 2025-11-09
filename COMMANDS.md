# 🎬 Movie Recommendation System - Command Cheat Sheet

## 🚀 Quick Start Commands

### First Time Setup

#### Backend (Terminal 1)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# OR
venv\Scripts\activate              # Windows

pip install -r requirements.txt
python utils/data_loader.py        # Import movie data (first time only)
python app.py                      # Start server
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

---

## 🔄 Daily Development Commands

### Backend
```bash
# Activate environment
cd backend
source venv/bin/activate           # macOS/Linux

# Start server
python app.py

# Reimport data (if needed)
python utils/data_loader.py

# Deactivate environment
deactivate
```

### Frontend
```bash
# Start development server
cd frontend
npm start

# Build for production
npm run build

# Install new package
npm install package-name
```

---

## 🧪 Testing Commands

### Backend API Tests
```bash
# Health check
curl http://localhost:5000/api/health

# Get all movies
curl http://localhost:5000/api/movies

# Get movies with search
curl "http://localhost:5000/api/movies?search=dark"

# Get movies by genre
curl "http://localhost:5000/api/movies?genre=Action"

# Get all genres
curl http://localhost:5000/api/genres

# Get single movie
curl http://localhost:5000/api/movies/the_dark_knight_2008

# Record a watch
curl -X POST http://localhost:5000/api/watch \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","movie_id":"inception_2010","completed":true}'

# Submit a rating
curl -X POST http://localhost:5000/api/rate \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","movie_id":"inception_2010","rating":5}'

# Get watch history
curl http://localhost:5000/api/watch-history/user123

# Get ratings
curl http://localhost:5000/api/ratings/user123

# Get recommendations
curl http://localhost:5000/api/recommendations/user123

# Get user activity
curl http://localhost:5000/api/user/user123/activity
```

---

## 🔧 Troubleshooting Commands

### Check Python Version
```bash
python3 --version
# Should be 3.8 or higher
```

### Check Node Version
```bash
node --version
# Should be 14 or higher
```

### Check if Backend is Running
```bash
curl http://localhost:5000/api/health
# Should return: {"success":true,"message":"Movie Recommendation API is running!"}
```

### Check Database Connection
```bash
cd backend
source venv/bin/activate
python -c "from models.database import init_db; init_db()"
# Should print: "Database tables created successfully!"
```

### Reinstall Backend Dependencies
```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Reinstall Frontend Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Clear Frontend Cache
```bash
cd frontend
rm -rf build
npm start
```

---

## 📊 Database Commands

### Check Movie Count
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, Movie
db = get_db()
count = db.query(Movie).count()
print(f'Total movies: {count}')
db.close()
"
```

### Check Watch History Count
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, WatchHistory
db = get_db()
count = db.query(WatchHistory).count()
print(f'Total watches: {count}')
db.close()
"
```

### Check Ratings Count
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, Rating
db = get_db()
count = db.query(Rating).count()
print(f'Total ratings: {count}')
db.close()
"
```

### Reset Watch History
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, WatchHistory
db = get_db()
db.query(WatchHistory).delete()
db.commit()
print('Watch history cleared!')
db.close()
"
```

### Reset Ratings
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, Rating
db = get_db()
db.query(Rating).delete()
db.commit()
print('Ratings cleared!')
db.close()
"
```

---

## 🌐 Browser Testing

### Open Pages Directly
```bash
# Home page
open http://localhost:3000

# Recommendations page
open http://localhost:3000/recommendations

# Backend health check
open http://localhost:5000/api/health
```

---

## 📦 Git Commands (Optional)

### Initialize Git
```bash
cd /Users/salmanhussain/Downloads/MovieRecommendatiion
git init
git add .
git commit -m "Initial commit: Movie Recommendation System"
```

### Check Status
```bash
git status
```

### Create Branch
```bash
git checkout -b feature/new-feature
```

### Push to GitHub (after creating repo)
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 🔥 Quick Restart

### Restart Backend
```bash
# In backend terminal, press Ctrl+C to stop
# Then:
python app.py
```

### Restart Frontend
```bash
# In frontend terminal, press Ctrl+C to stop
# Then:
npm start
```

### Restart Both
```bash
# Terminal 1
cd backend && source venv/bin/activate && python app.py

# Terminal 2
cd frontend && npm start
```

---

## 📝 Useful Shortcuts

### Kill Process on Port
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Check Ports
```bash
# Check what's running on port 5000
lsof -i :5000

# Check what's running on port 3000
lsof -i :3000
```

### View Logs
```bash
# Backend logs (if running in background)
tail -f backend.log

# Frontend logs (if running in background)
tail -f frontend.log
```

---

## 🎯 One-Line Setups

### Complete First-Time Setup
```bash
# Run in project root directory
(cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python utils/data_loader.py) && (cd frontend && npm install)
```

### Start Both Servers (after setup)
```bash
# Terminal 1
cd backend && source venv/bin/activate && python app.py

# Terminal 2
cd frontend && npm start
```

---

## 💾 Backup Commands

### Backup Database Data
```bash
# Export watch history
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, WatchHistory
import json
db = get_db()
watches = [w.to_dict() for w in db.query(WatchHistory).all()]
with open('backup_watches.json', 'w') as f:
    json.dump(watches, f, indent=2, default=str)
print('Watch history backed up!')
db.close()
"
```

### Backup Project (without dependencies)
```bash
cd /Users/salmanhussain/Downloads
tar -czf MovieRecommendation_backup.tar.gz \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='__pycache__' \
  MovieRecommendatiion/
```

---

## 🚀 Performance Testing

### Load Test Backend
```bash
# Install Apache Bench (if not installed)
# brew install httpd (macOS)

# Test movies endpoint
ab -n 100 -c 10 http://localhost:5000/api/movies

# Test recommendations endpoint
ab -n 50 -c 5 http://localhost:5000/api/recommendations/user123
```

---

## 📊 Monitoring

### Watch Backend Logs
```bash
cd backend
source venv/bin/activate
python app.py | tee backend.log
```

### Monitor System Resources
```bash
# Monitor CPU and memory
top

# Monitor network
netstat -an | grep LISTEN
```

---

## 🎓 Demo Preparation

### Quick Demo Setup
```bash
# Terminal 1: Start backend
cd backend && source venv/bin/activate && python app.py

# Terminal 2: Start frontend
cd frontend && npm start

# Terminal 3: Open browser
open http://localhost:3000
```

### Reset for Fresh Demo
```bash
cd backend
source venv/bin/activate
python -c "
from models.database import get_db, WatchHistory, Rating
db = get_db()
db.query(WatchHistory).delete()
db.query(Rating).delete()
db.commit()
print('Demo reset complete! Ready for fresh demo.')
db.close()
"
```

---

## 📚 Reference

### API Base URL
```
http://localhost:5000
```

### Frontend URL
```
http://localhost:3000
```

### Database URL (configured in .env)
```
postgresql://neondb_owner:npg_wBLldE74pimx@ep-sweet-thunder-adgkv27e-pooler.c-2.us-east-1.aws.neon.tech/movie_recom?sslmode=require&channel_binding=require
```

### Default User ID
```
user123
```

---

**Save this file for quick reference! 📌**
