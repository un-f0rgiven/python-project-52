dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	poetry run gunicorn task_manager.wsgi:application

test:
	poetry run pytest

lint:
	poetry run flake8