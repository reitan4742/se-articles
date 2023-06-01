run:
		python3 manage.py runserver
type:
		mypy --config-file mypy.ini --ignore-missing-imports .
strict:
		mypy --strict --config-file mypy.ini .
test:
		python manage.py test self_introduction
reset:
		rm articles/migrations/0001_initial.py
		rm -r articles/migrations/__pycache__
		rm db.sqlite3

db:
		python manage.py makemigrations
		python manage.py migrate
		python manage.py createsuperuser