#!/usr/bin/bash

cd /home/dima/sites/www.staging.beget-django-deployment-test.online
source ./venv/bin/activate
cd DjangoDeploymentTest/Website
gunicorn --bind unix:/tmp/staging.beget-django-deployment-test.online.socket Website.wsgi:application  