@echo off
python reset.py %*
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --email msname@live.ru --username m7Name
python manage.py runserver
