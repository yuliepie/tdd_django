# First steps
- Install django and DRF
- Create boilerplate django-admin project
- Create movies app package from Django CLI
```shell
(env)$ pip install django==4.0 djangorestframework==3.13.1
(env)$ django-admin startproject drf_project .
(env)$ python manage.py startapp movies
```
- Add DRF & movies to `INSTALLED_APPS` in `settings.py`

## Migration
- Create custom user model (`settings.py` & `models.py`)
- Create migration file & apply migrations to sqlite DB
```shell
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
- Check file is created in `migrations` folder
- Check `CustomUser` class is being used as the default User class, by inspecting with SQLite shell
```shell
$ sqlite3 db.sqlite3 # enter SQLite shell

sqlite> .tables # show tables

sqlite> .schema movies_customuser # check table fields

sqlite> .exit
```

## Run Development Server
- Create superuser. This user can login to the admin site.
- e.g. `admin & yulieadmin`
```shell
(env)$ python manage.py createsuperuser
(env)$ python manage.py runserver
```
- navigate to `http://localhost:8000/admin/` to view django admin page (CMS) with superuser credentials

## Docker
- Create Dockerfile that loads app to container. Set docker-compose to build app service with appropriate .env file.
- view dev server at `localhost:8009`
```shell
docker-compose build
docker-compose up -d

docker-compose logs -f # view logs

docker-compose down -v # Bring down container incl. volume
```
## Postgres DB
- add postgresDB service to docker-compose (set default user and DB name)
- add env variables for django to communicate with postgresDB container, and link those env variables in `settings.py`
- install postgres dependency for docker app service
- add Psycopg2 postgresDB driver to requirements.txt
- Build image and spin up containers: `docker-compose up -d --build`
- Run migrations to new postgresDB: `docker-compose exec movies python manage.py migrate --noinput`
  - *NOTE*: if migration causes error due to Mac M1, build docker platform on linux by including in docker-compose service argument: `platform: linux/amd64`
- available on default port `5432` for other services

### Checking with psql command
```shell
$ docker-compose exec movies-db psql --username=movies --dbname=movies_dev

# list databases
\l

# connect to movies_dev DB
\c movies_dev

# list of tables
\dt

#quit
\q
```
- Check volume for DB is created: (host_volumename)
```
docker volume inspect django-tdd-docker_postgres_data
```
## Entrypoint script
- On movies service startup, wait for postgres container to be available in `entrypoint.sh` file
- Once postgres available, run the migration script (in the file)
- Update file permissions locally: `$ chmod +x app/entrypoint.sh`
- Update Dockerfile to include dependency (netcat) for running entrypoint file, and copy and run the file
### Check everything works:
- `docker-compose up -d --build`
- navigate to localhost:8009

# Pytest
- pytest discovers test files that start or end with `test`
  - Test functions must begin with `test_`
  - Test classes must also begin with `Test`
- Unlike unittest, pytest does not need Test classes. Test functions just work
- `pytest.ini` file: define `DJANG_SETTINGS_MODULE` variable to point to Django settings file & test discovery rules
- After adding pytest as requirement, rebuild docker images
### Running Tests
- Run tests: `docker-compose exec movies pytest`
- e.g. run tests with `models` in their names:
```shell
docker-compose exec movies pytest -k models
```
### Test requiring database
- Mark tests that require database access with `@pytest.mark.django_db`
- Ensures DB is setup correctly before the test
- Test will run a db transaction which will be **rolled back after the test completes**.

# Django REST Framework (DRF)
- full-featured API framework to build REST APIs with Django
- Composed of:
- **Serializers**: converts Django querysets and model instances to and from JSON (serialization & deserialization)
- **Views**: 
  - Classes/Functions that handle HTTP requests and return serialized data as HTTP response. View uses serializers to validate incoming payloads, and contains logic to return response.
  - Coupled with routers, which *map the views with URL endpoints*
  - ViewSets: a class that combines logic for related views. Similar to a Controller.

## Models
- Django ORM <-> database
- After creating models, make migrations & migrate
```shell
$ docker-compose exec movies python manage.py makemigrations

$ docker-compose exec movies python manage.py migrate
```
- Add to Django admin page in `admin.py`
  - Create superuser account
  - Login and add new movies

## Serializers
- converts django models <-> json
- Have to be created for each model (see MovieSerializer)
- Most serializers are tied to a model via the `ModelSerializer` class
  - ModelSerializer takes a particular model, and outputs all fields of the model, while dealing with read-only ones.
  - Can take json object as `data` parameter, and serialize the data into a **Django model instance**
  - Can save the serialized model into the db
- However, this doesn't mean ALL serializers need to be tied to a model. Some REST Apis may not need model data, right?

## Views
- DRF views are functions/classes that take HTTP requests and return HTTP responses
- 3 types: Views, ViewSets, Generic Views
### 1. Views
- Most basic DRF view type, subclasses Django's `View` class
- function: `@api_view` decorator
- class: `APIView` class
### 2. ViewSets
- layer of abstraction above views
- Combine CRUD operation logic into a single place
- Helps with URL consistency, minimizes code, helps focus on the API logic by simplifiying
- Good for basic CRUD operations, but not for complex API that does not map exactly to existing models
### 3. Generic Views
- Takes abstraction layer further
- One blueprint for several model APIs
- Infers response format, allowed API methods, payload shape - based on serializer
> This tutorial project uses the View type, using the `APIView` class

## URLs
- Define url endpoint patterns for the app in `movieApp/urls.py`
- Map API urls <-> Views
- Add app-specific URLs to the project level by updating `drf_project/urls.py`, like adding a blueprint in Flask
  - use the `include` functionality in django.urls

> TIP: sent HTTP requests from the command line with HTTPie
> `http --json POST http://localhost:8009/api/movies/ title=Fargo genre=comedy year=1996`