#!/bin/sh

#python manage.py flush --no-input
#python manage.py migrate
python manage.py check
env
#ls -l
echo  $@
eval $@