#!/bin/sh

#python manage.py flush --no-input
#python manage.py migrate
python manage.py check
#ls -l
echo  $@
eval $@