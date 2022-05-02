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