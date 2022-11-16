#!/bin/sh
#startup django container sequence
#python manage.py flush --no-input
#python manage.py migrate
python manage.py check
#python manage.py collectstatic
env
echo  $@
eval $@