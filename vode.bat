@echo off
set run=%1

if "%run%"=="-r" python manage.py runserver
if "%run%"=="-R" python -m gunicorn --reload --log-level debug wooden.asgi:application -k uvicorn.workers.UvicornWorker
if "%run%"=="-s" python manage.py shell
if "%run%"=="-d" docker run --rm -p 6379:6379 redis:latest
if "%run%"=="-mm" python manage.py makemigrations
if "%run%"=="-m" python manage.py migrate
if "%run%"=="-a" call ..\env\Scripts\activate.bat
if "%run%"=="-c" python manage.py check
if "%run%"=="-cd" python manage.py check --deploy
if "%run%"=="-st" python manage.py collectstatic --noinput
