run:
	python3 manage.py runserver
startapp:
	python manage.py startapp $(name) && mv $(name) apps/$(name)
migration:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
no-db:
	rm -rf db.sqlite3
re-django:
	pip3 uninstall Django -y && pip3 install Django
cru:
	#make cru email=goldendevuz@gmail.com birth=2005-01-24
	python manage.py createsuperuser --email $(email) --birth_date=$(birth)