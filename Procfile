release: python manage.py migrate --noinput
web: gunicorn toporahma_project.wsgi:application --log-file -
