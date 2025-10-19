# Quick Heroku Command Reference

## Initial Setup
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set GEMINI_API_KEY="your-key"
heroku config:set ELEVENLABS_API_KEY="your-key"
```

## Deployment
```bash
# Deploy current branch
git push heroku heroku-deployment:main

# Or if on main branch
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

## Monitoring & Debugging
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Check config
heroku config

# Open app in browser
heroku open

# Restart app
heroku restart
```

## Database
```bash
# Access database info
heroku pg:info

# Open database console
heroku pg:psql

# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download
```

## Scaling
```bash
# Scale web dynos
heroku ps:scale web=1

# Check dyno type
heroku ps:type

# Upgrade dyno
heroku ps:type web=basic
```

## Django Management
```bash
# Run any Django command
heroku run python manage.py <command>

# Django shell
heroku run python manage.py shell

# Load fixtures
heroku run python manage.py loaddata <fixture>
```

## Troubleshooting
```bash
# Check buildpack
heroku buildpacks

# Clear cache
heroku plugins:install heroku-repo
heroku repo:purge_cache -a your-app-name

# One-off dyno (for debugging)
heroku run bash
```
