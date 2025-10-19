#!/bin/bash
run=$1

declare -A commands=(
    ["-r"]="python manage.py runserver"
    ["-R"]="python -m gunicorn --reload --log-level debug wooden.asgi:application -k uvicorn.workers.UvicornWorker"
    ["-s"]="python manage.py shell"
    ["-d"]="docker run --rm -p 6379:6379 redis:latest"
    ["-mm"]="python manage.py makemigrations"
    ["-m"]="python manage.py migrate"
    ["-a"]="source ../env/bin/activate"
    ["-c"]="python manage.py check"
    ["-cd"]="python manage.py check --deploy"
    ["-st"]="python manage.py collectstatic --noinput"
)

if [[ -n "${commands[$run]}" ]]; then
    eval "${commands[$run]}"
else
    echo "Invalid option. Please use one of the following: ${!commands[@]}"
fi
