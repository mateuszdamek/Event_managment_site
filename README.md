# Installation
Needed modules:
- Django  
- RestFramework
- Corsheaders
- Socialauth for Google auth

## Windows:
Commands cmd:
```
$ pip install django
$ pip install djangorestframework
$ pip install django-cors-headers
$ pip install django-allauth
```
********************************
## Linux/MacOS:
Project files should be in created venv

Commands terminal:
```
$ python -m venv myenv
$ source myenv/bin/activate
$ pip install django
$ pip install djangorestframework
$ pip install django-cors-headers
$ pip install django-allauth
```
Eventually, if you finished project, deactivate virtual environment:
```
$ deactivate
```

## Running project

Backend
```
$ cd source/backend/Event/
$ py manage.py runserver /Alternatively/ python3 manage.py runserver
```
Frontend
```
$ cd source/backend/Frontend/
$ yarn dev
```

