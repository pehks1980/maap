import os
from pathlib import Path

BASE_DIR1 = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    #'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

     'default': {
         'NAME': 'maap',
         'ENGINE': 'django.db.backends.postgresql',
         'USER': 'maap',
         'PASSWORD': 'maap',
         'HOST': '192.168.1.204'
     }
}