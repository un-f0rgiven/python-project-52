dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	@if [ -z "$$PORT" ]; then echo "Ошибка: Переменная окружения PORT не задана!"; exit 1; fi
	poetry run gunicorn task_manager.wsgi:application

test:
	poetry run pytest

lint:
	poetry run flake8

build:
	./build.sh 