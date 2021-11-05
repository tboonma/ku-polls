web: gunicorn mysite.wsgi:application
release: python manage.py migrate --run-syncdb
python3 manage.py loaddata users polls
