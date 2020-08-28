"""
Django settings for maap project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e2nsv_7ja12&g=x5amt(ojd4b5o8&oi8g#3kpfk#xnnav490)4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '192.168.1.100']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'db_file_storage',
    'mainapp',
    'authapp',
    'django_cron',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CRON_CLASSES = [
    'cron.MyCronJob',
    # ...
]
ROOT_URLCONF = 'maap.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'maap.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'NAME': 'maap_bk',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'maap',
        'PASSWORD': 'maap',
        'HOST': '192.168.1.200'
    }


}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/staticfiles/'

STATICFILES_DIRS = (
    'staticfiles',
    os.path.join(BASE_DIR, 'staticfiles'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'authapp.MaapUser'  # our auth instaed of USER model

LOGIN_URL = '/auth/login/'

DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

#additional path settings for gunicorn when deployment
import sys
sys.path.append('/home/user/django/maap/mainapp')
sys.path.append('/home/user/django')
#print (sys.path)

#app settings
NX = 12 #models.PositiveIntegerField(verbose_name='nx', default=12)
NY = 10 #models.PositiveIntegerField(verbose_name='ny', default=10)

AX = 100 #models.PositiveIntegerField(verbose_name='ax', default=100)
SX = 100 #models.PositiveIntegerField(verbose_name='sx', default=100)

TWO_DIGIT  = 1 #two_digit = models.PositiveIntegerField(verbose_name='two_digit', default=1)
NO_MINUS = 1 #no_minus = models.PositiveIntegerField(verbose_name='no_minus', default=1)
NO_DEC_MUL = 1 #no_dec_mul = models.PositiveIntegerField(verbose_name='no_dec_mul', default=1)
HIST_DEPTH = 10 #hist_depth = models.PositiveIntegerField(verbose_name='hist_depth', default=5)
FAVOR_THRESOLD_TIME = 15 #favor_thresold_time = models.PositiveIntegerField(verbose_name='hist_depth', default=15)

