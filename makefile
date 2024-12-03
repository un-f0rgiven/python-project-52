dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

test:
	poetry run pytest

lint:
	poetry run flake8

build:
	./build.sh 