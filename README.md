# Django Blog
[![Django CI](https://github.com/azisyulianas/djangoblog/actions/workflows/django.yml/badge.svg)](https://github.com/azisyulianas/djangoblog/actions/workflows/django.yml)


# Intalations

```bash 
    git clone https://github.com/azisyulianas/djangoblog.git 
    py -m venv venv 
    \venv\Scripts\activate 
    py install -r requirements.txt 
    py manage.py makemigrations 
    py manage.py migrate 
    py manage.py createsuperuser 
    py manage.py runserver 
```

after that open browser and open this link
http://127.0.0.1:8000/admin/
login with your create super user before

open `Groups` and add group `author` and `admin` 
open `User posts` add your `super user` in that table 