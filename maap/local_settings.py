import os
from pathlib import Path

BASE_DIR1 = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '12345'
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True
DEBUG = os.environ.get("DEBUG")


ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    #'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

     # 'default': {
     #     'NAME': 'maap_test',
     #     'ENGINE': 'django.db.backends.postgresql',
     #     'USER': 'maap',
     #     'PASSWORD': 'maap',
     #     'HOST': '192.168.1.204'
     # }

    # env version
    'default': {
         'NAME': os.environ.get("SQL_DATABASE"),
         'ENGINE': 'django.db.backends.postgresql',
         'USER': os.environ.get("SQL_USER"),
         'PASSWORD': os.environ.get("SQL_PASSWORD"),
         'HOST': os.environ.get("SQL_HOST")
     }

}
