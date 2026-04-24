# ShambaApp: A Farmer Management Information System

A full-stack web application for managing farmers, built with Django REST Framework and HTML/CSS/JS.

## Tech Stack

|------------|-------------------------------------|
| Backend    | Django 4.2 + Django REST Framework  |
| Frontend   | HTML, CSS, JavaScript         |
| Database   | SQLite (development), PostgreSQL (production) |
| Auth       | JWT |
| Weather API| OpenWeatherMap |
| Backend hosting | Render         |
| Frontend hosting | Netlify          |

## Backend API Reference

|------------|---------|-------------------------------------------------|
| Method | Endpoint| AuthDescription |
| POST| /api/auth/register/ | None| Register user |
| POST| /api/auth/login/| None| Login → returns JWT |
| POST | /api/auth/refresh/| None| Refresh access token |
| POST| /api/auth/logout/| JWT| Blacklist refresh token |
| GET| /api/auth/me/| JWT| Current user info |
| GET| /api/farmers/dashboard/admin/ | Admin JWT| Admin dashboard |
| GET | /api/farmers/dashboard/farmer/ | Farmer JWT | Farmer dashboard + weather |
| GET | /api/farmers/ | Admin JWT | List all farmers |
| POST | /api/farmers/ | Admin JWT | Add a farmer |
| GET | /api/farmers/<id>/ | Admin JWT | Get farmer detail |
| PUT/PATCH | /api/farmers/<id>/ | Admin JWT | Edit a farmer |
| DELETE | /api/farmers/<id>/ | Admin JWT | Delete a farmer |

## Authentication Method

- Email + password login
- Passwords hashed by Django's `AbstractBaseUser` 
- On login, API returns a short-lived **access token** (1 hour) and a long-lived **refresh token** (7 days)
- The frontend stores tokens in `localStorage` and automatically refreshes the access token when it expires
- Logout blacklists the refresh token server-side so it cannot be reused

## API Used

**OpenWeatherMap — Current Weather Data**
- Endpoint: `https://api.openweathermap.org/data/2.5/weather`
- When a farmer visits their dashboard, the API fetches live weather for the city stored in their profile. A rule-based engine then generates a crop-specific insights based on that weather.

## Design Decisions

- **Custom User model** with a `role` field (admin/farmer) instead of Django groups keeps role checks simple.
- **JWT over session auth** because the frontend is served separately (Netlify) from the API (Render).
- **SQLite in dev, PostgreSQL in prod** — switched automatically via the `DATABASE_URL` env variable.
- **WhiteNoise** serves Django's static files in production without needing a CDN or nginx.

## Local Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/P-Alakara/FARMER-MIS.git
cd FARMER-MIS

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
touch .env
# Edit .env and fill in SECRET_KEY and OPENWEATHER_API_KEY

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. Start Django
python manage.py runserver

# 8. Open the frontend (in a separate terminal)
cd frontend
python -m http.server 5500
# Visit http://127.0.0.1:5500
```

## Deployment
Site Link: https://shamba-app.netlify.app/
