# 🚀 Local Development Guide

## First Time Setup

### 1. Create Virtual Environment (Recommended)
```bash
# Using Python's venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API keys:
# - GEMINI_API_KEY
# - ELEVENLABS_API_KEY
# - (Optional) CLOUDFLARE_API_KEY and CLOUDFLARE_ACCOUNT_ID
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Create Test Data (Optional)
```bash
python manage.py shell
# Then run commands to create test candidates, roles, etc.
```

## Daily Development

### Start Development Server
```bash
# Make sure virtual environment is activated
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

### Access Admin Panel
```
http://127.0.0.1:8000/admin/
```

## Testing Production Setup Locally

### 1. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 2. Run with Gunicorn (Production Server)
```bash
# Install gunicorn if not already installed
pip install gunicorn

# Run with gunicorn
gunicorn vode.wsgi:application --bind 0.0.0.0:8000
```

## Common Commands

### Database
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (careful!)
del db.sqlite3
python manage.py migrate
```

### Django Shell
```bash
python manage.py shell
```

### Create Sample Data
```python
# In Django shell
from django.contrib.auth.models import User
from cand.models import Candidate
from swe.models import SWE
from recruit.models import Recruiter

# Create users and related objects
```

### Run Tests
```bash
python manage.py test
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
- Make sure you activated your virtual environment
- Run: `pip install -r requirements.txt`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check STATIC_URL and STATICFILES_DIRS in settings.py

### Database Errors
- Delete db.sqlite3 and run migrations again
- Make sure migrations are up to date

### API Keys Not Working
- Check your .env file exists and has correct values
- Make sure python-dotenv is installed
- Restart the server after changing .env

## File Structure
```
vode/
├── cand/           # Candidate app
├── interview/      # Interview app
├── recruit/        # Recruiter app
├── swe/            # Software Engineer app
├── static/         # Static files (CSS, JS)
├── templates/      # HTML templates
├── vode/           # Main project settings
├── db.sqlite3      # SQLite database (local only)
├── manage.py       # Django management script
└── requirements.txt # Python dependencies
```

## Environment Variables Required

**Local Development (.env file):**
```
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
```

**Production (Heroku):**
- All of the above
- DATABASE_URL (automatically set by Heroku)
- DEBUG=False

## Next Steps

1. **Start the server**: `python manage.py runserver`
2. **Open browser**: http://127.0.0.1:8000/
3. **Check admin panel**: http://127.0.0.1:8000/admin/
4. **Create test data**: Use admin panel or Django shell

## Quick Start (Copy/Paste)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up .env file (edit with your API keys)
copy .env.example .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## URLs
- Home/Candidate Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Candidate: http://127.0.0.1:8000/candidate/
- Recruiter: http://127.0.0.1:8000/recruiter/
- SWE: http://127.0.0.1:8000/swe/
- Interview: http://127.0.0.1:8000/interview/{id}/
