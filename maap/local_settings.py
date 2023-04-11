import datetime
import os
from pathlib import Path

BASE_DIR1 = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

#SECRET_KEY = '12345'

SECRET_KEY = os.environ.get("SECRET_KEY")
import subprocess

if SECRET_KEY == None:
    #load dev.env file in case no environment for debug purposes
    env_vars = {'MY_VAR': 'value'}
    with open(".env.dev") as f:
        for line in f:
            if line[0] != '#':
                (key, val) = line.rstrip().split(sep='=')
                env_vars[key] = val

    SECRET_KEY = env_vars.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True
DEBUG = os.environ.get("DEBUG")
if DEBUG == None:
    DEBUG = env_vars.get('DEBUG')

#only one value sorry
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS == None:
    ALLOWED_HOSTS = env_vars.get('ALLOWED_HOSTS')

#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#as per cred_maap sendmail
HOST_URL = os.environ.get("HOST_URL")
SENDER_MAIL = os.environ.get("SENDER_MAIL")
MAIL_ACCT = os.environ.get("MAIL_ACCT")
MAIL_PASSWD = os.environ.get("MAIL_PASSWD")
MAIL_ACC_TOKEN = os.environ.get("MAIL_ACC_TOKEN")
CLIENT_ID = os.environ.get("MAIL_ACC_TOKEN")

PROBE_TEST = os.environ.get("PROBE_TEST")
if PROBE_TEST == None:
    PROBE_TEST = env_vars.get('PROBE_TEST')
PROBE_TEST = int(PROBE_TEST)

START_DATE = datetime.datetime.now()
GIT_COMMIT = os.environ.get("GIT_COMMIT")
print("========== START =============== GIT_COMMIT: ", GIT_COMMIT, " ============ START =============")
myenv = dict(sorted(os.environ.items()))
for name, value in myenv.items():
    if name.find('PASS') != -1 or name.find('SECRET') != -1:
        print("{0}: {1}".format(name, '*********'))
    else:
        print("{0}: {1}".format(name, value))

SQL_DATABASE = os.environ.get("SQL_DATABASE")
if  SQL_DATABASE == None:
     SQL_DATABASE = env_vars.get('SQL_DATABASE')

SQL_USER = os.environ.get("SQL_USER")
if SQL_USER == None:
    SQL_USER = env_vars.get('SQL_USER')

SQL_PASSWORD = os.environ.get("SQL_PASSWORD")
if SQL_PASSWORD == None:
    SQL_PASSWORD = env_vars.get('SQL_PASSWORD')

SQL_HOST = os.environ.get("SQL_HOST")
if SQL_HOST == None:
   SQL_HOST = env_vars.get('SQL_HOST')

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
         'NAME': SQL_DATABASE,
         'ENGINE': 'django.db.backends.postgresql',
         'USER': SQL_USER,
         'PASSWORD': SQL_PASSWORD,
         'HOST': SQL_HOST
     }

}
