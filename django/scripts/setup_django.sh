#!/bin/bash

##########################################################
#### Taking care of mariadb service and configuration ####
##########################################################
echo "[INFO] : Starting mysql service"
service mysql start

#Setup Django application database and users
echo "[INFO] : Setting up database"
mysql -e 'CREATE DATABASE IF NOT EXISTS matchdata'
mysql -e "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123'"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';"

##########################################################
#### Taking care of Django setup and code deployment #####
##########################################################

##New project generation
echo "[INFO] : Generating project"
cd /opt/django && django-admin startproject challenger
mv /opt/django/challenger /opt/django/src

#Code deployment over vanila created app 
echo "[INFO] : Code deploying"
cp -Rf /root/src/* /opt/django/src
chown -R www-data:www-data /opt/django/src
chmod -R 755 /opt/django/src

##Django database initialization
echo "[INFO] : Re-running migrations"
/opt/django/src/manage.py makemigrations
/opt/django/src/manage.py migrate

##Admin user creation
echo "[INFO] : Admin user creation"
cat <<EOF | python /opt/django/src/manage.py shell
from django.contrib.auth.models import User
User.objects.filter(username="admin").exists() or User.objects.create_superuser("admin", "admin@example.com", "admin123")
EOF

##########################################################
############ Starting apache service #####################
##########################################################
echo "[INFO] : Starting apache service"
#service apache2 start
apache2ctl -D "FOREGROUND"

