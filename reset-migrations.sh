find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "*/django/*" -delete
find . -path "*/migrations/*.pyc" -not -path "*/django/*" -delete

rm db.sqlite3

python manage.py makemigrations
python manage.py migrate