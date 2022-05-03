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