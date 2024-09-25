gen-env:
	python3 -m venv env && . env/bin/activate
migrate:
	python3 manage.py migrate
run:
	python3 manage.py runserver 8000
i:
	pip install -r requirements/base.txt
freeze:
	pip freeze > requirements.txt
cru:
	#  python manage.py createsuperuser --username admin --email admin@example.com
	python manage.py createsuperuser --username superuser --email superuser@example.com
migration:
	python3 manage.py makemigrations
create-not-author:
	python manage.py createuser --username notauthor --email notauthor@example.com --password 1
create-author:
	python manage.py createuser --username author --email author@example.com --password 1
collect:
	python manage.py collectstatic --noinput
clear:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete
	#rm -rf db.sqlite3
re-django:
	pip3 uninstall Django && pip3 install Django
startapp:
	python manage.py startapp $(name) && mv $(name) apps/$(name)