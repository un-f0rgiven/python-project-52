dev:
	poetry run python manage.py runserver

install:
	poetry install

PORT ?= 10000

start:
	poetry install
	@if [ -z "$$PORT" ]; then echo "Ошибка: Переменная окружения PORT не задана!"; exit 1; fi
	poetry run python manage.py migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$$PORT task_manager.wsgi:application

test:
	poetry run python manage.py test

lint:
	poetry run flake8

build:
	./build.sh

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate