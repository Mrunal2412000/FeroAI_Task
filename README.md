# FeroAI_Task

## Index

- [Index](#index)
- [Introduction](#introduction)
- [Installation](#installation)

### Introduction

- Supports latest version of Python along with Django
- Authentication APIs are introduced to boost the development speed.
- Swagger integration available to prepare APIs documentation.
- Swagger docummentation is ready to use for all the pre-implemented APIs.


### Installation

> ##### 1. Clone repository


git clone https://github.com/Mrunal2412000/FeroAI_Task.git


> ##### 2. If you are not having pip and Django, let's install

sudo easy_install pip

python -m pip install Django

> ##### 3. Create virtual environment and activate

pipenv shell

> ##### 4. Setup The Project


pipenv install -r requirements.txt

> ##### 5. Create Database Manuanlly in PgAdmin

CREATE DATABASE <database_name>

> ##### 6. Setting up your database details in .env, also added .env_example for reference

DB_NAME=DATABASE_NAME

DB_USER=DATABASE_USER

DB_PASSWORD=DATABASE_PASSWORD

DB_HOST=HOST_NAME

DB_PORT=PORT_NUMBER

> ##### 7. Setting up your Swagger Server Url in .env

SWAGGER_SERVER= i.e - "http://127.0.0.1:8000"

> ##### 8. Create tables by Django migration

python manage.py makemigrations

python manage.py migrate

> ##### 9. Admin panel will be available @ `/admin`

For client use, You can create superuser manually by running this command "python manage.py createsuperuser"

> ##### 10. Swagger UI will be available @ `/swagger-ui`