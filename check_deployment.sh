#!/bin/bash
# Quick deployment check script

echo "🔍 Checking Heroku Deployment Requirements..."
echo ""

# Check if files exist
files=(
    "Procfile"
    "runtime.txt"
    "requirements.txt"
    "app.json"
    ".python-version"
    "manage.py"
    "vode/settings.py"
    "vode/wsgi.py"
)

all_good=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (MISSING)"
        all_good=false
    fi
done

echo ""
echo "🔧 Checking Python Packages..."

# Check if requirements.txt has required packages
required_packages=(
    "gunicorn"
    "whitenoise"
    "dj-database-url"
    "psycopg2-binary"
    "Django"
)

for package in "${required_packages[@]}"; do
    if grep -q "$package" requirements.txt 2>/dev/null; then
        echo "✅ $package"
    else
        echo "❌ $package (MISSING FROM requirements.txt)"
        all_good=false
    fi
done

echo ""
if [ "$all_good" = true ]; then
    echo "✅ All checks passed! Ready for deployment."
    echo ""
    echo "Next steps:"
    echo "1. heroku create your-app-name"
    echo "2. heroku addons:create heroku-postgresql:essential-0"
    echo "3. heroku config:set SECRET_KEY=\$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
    echo "4. heroku config:set DEBUG=False"
    echo "5. heroku config:set GEMINI_API_KEY=your_key"
    echo "6. heroku config:set ELEVENLABS_API_KEY=your_key"
    echo "7. git push heroku heroku-deployment:main"
else
    echo "❌ Some checks failed. Please fix the issues above."
fi
