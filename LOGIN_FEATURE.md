# Login & User Authentication

## Overview
The Movie Recommendation System now includes user authentication to provide personalized recommendations for each user.

## Features

### Login Page
- **Custom User ID**: Users can enter their own unique user ID
- **Demo Users**: Quick login with pre-configured demo accounts:
  - Alice
  - Bob
  - Charlie
- **Validation**: User IDs must be alphanumeric (letters, numbers, underscores, and hyphens only)

### Protected Routes
All application pages (Browse, Recommendations) are protected and require login:
- Unauthenticated users are redirected to the login page
- Authenticated users can access all features

### User Session
- User ID is stored in browser's localStorage
- Session persists across page refreshes
- Logout button available in the header

## Usage

### First Time Users
1. Navigate to http://localhost:3000
2. You'll be automatically redirected to `/login`
3. Enter a unique user ID or click a demo user button
4. Start browsing and rating movies!

### Returning Users
- Your session is saved in localStorage
- Simply open the app and continue where you left off
- Use the logout button to switch users

### API Integration
All API calls now use the current logged-in user's ID:
- Watch history is tracked per user
- Ratings are saved per user
- Recommendations are personalized per user

## User Data Isolation
Each user has their own:
- Watch history
- Movie ratings
- Personalized recommendations

This ensures that recommendations are truly personalized based on individual viewing habits and preferences.

## Technical Details

### Frontend Files
- `LoginPage.js` - Login page component
- `LoginPage.css` - Login page styling
- `ProtectedRoute.js` - Route guard component
- `auth.js` - Authentication utility functions
- Updated `App.js` - Route configuration with authentication
- Updated `Header.js` - User display and logout functionality
- Updated `api.js` - Dynamic user ID for all API calls

### Authentication Flow
1. User enters credentials on login page
2. User ID is validated and stored in localStorage
3. User is redirected to browse page
4. All subsequent API calls use the stored user ID
5. Logout clears localStorage and redirects to login

## Development Notes
- User IDs are stored client-side (no server-side authentication)
- This is a simplified authentication for demo purposes
- In production, implement proper authentication with JWT tokens or sessions
- Add password protection for real-world use
