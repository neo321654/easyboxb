up:
	docker-compose up -d --build

down:
	docker-compose down

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

