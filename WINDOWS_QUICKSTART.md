# 🚀 Quick Start Guide - Windows

## For Local Development (Your Computer)

### Step 1: Install Development Dependencies (No PostgreSQL needed!)
```bash
pip install -r requirements-dev.txt
```

**OR** if you're using the virtual environment:
```bash
C:/Users/enesi/Code/hacktx2025/env/Scripts/python.exe -m pip install -r requirements-dev.txt
```

### Step 2: Set Up Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API keys
```

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Start the Server
```bash
python manage.py runserver
```

**Your app will be running at: http://127.0.0.1:8000/**

---

## For Heroku Deployment (Production)

Heroku will automatically install `psycopg2-binary` from `requirements.txt` because it has PostgreSQL installed. Your local Windows machine doesn't need it!

### Deploy to Heroku:
```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 4. Set environment variables
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set DEBUG=False
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set ELEVENLABS_API_KEY=your_key_here

# 5. Deploy
git push heroku heroku-deployment:main

# 6. Run migrations
heroku run python manage.py migrate

# 7. Open app
heroku open
```

---

## Why Two Requirements Files?

**requirements-dev.txt** (Local Development):
- ✅ Django, requests, google-generativeai, etc.
- ❌ No psycopg2-binary (PostgreSQL)
- ✅ Uses SQLite database (built into Python)
- ✅ Installs easily on Windows

**requirements.txt** (Production/Heroku):
- ✅ Everything from requirements-dev.txt
- ✅ gunicorn (production server)
- ✅ whitenoise (static files)
- ✅ psycopg2-binary (PostgreSQL - Heroku installs this)
- ✅ dj-database-url (PostgreSQL connection)

---

## Troubleshooting

### ❌ Error: "pg_config executable not found"
**Solution**: Use `requirements-dev.txt` for local development:
```bash
pip install -r requirements-dev.txt
```

### ❌ Error: "No module named 'django'"
**Solution**: Make sure you installed dependencies:
```bash
pip install -r requirements-dev.txt
```

### ❌ Database errors on Heroku
**Solution**: Run migrations on Heroku:
```bash
heroku run python manage.py migrate
```

---

## Summary

**Local (Windows)**: 
```bash
pip install -r requirements-dev.txt
python manage.py runserver
```

**Production (Heroku)**:
```bash
git push heroku heroku-deployment:main
```

Heroku automatically uses `requirements.txt` and installs PostgreSQL properly! 🎉
