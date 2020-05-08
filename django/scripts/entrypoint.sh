#!/bin/bash

##########################################################
### Waiting for mysql service start and configuration  ###
##########################################################

#mysql service may take sometime to get started
while ! $(/usr/bin/mysql -h mariadb -u admin -padmin123 -e "status" 2>/dev/null 1>/dev/null); do
    echo "[INFO] : MySQL service is not available ... can take time up to few minutes ... sleeping for 3 sec ..." 
    sleep 3
done

echo "[INFO] : MySQL creating django database"
mysql -h mariadb -u root -padmin123 -e "CREATE DATABASE IF NOT EXISTS matchdata;"

echo "[INFO] : MySQL granting preveliges for admin user"
mysql -h mariadb -u root -padmin123 -e "grant all privileges on *.* to 'admin'@'%';"



################################################
#### Taking care of Django db configration #####
################################################

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

#Collect static files
echo "[INFO] : Collecting statics"
/opt/django/src/manage.py collectstatic --noinput

#########################################################
############# Entering main loop ########################
#########################################################

#start pika messages listener as a daemon
echo "[INFO] : Initialising pconsumer message listenr"
/usr/local/bin/python /opt/django/src/pikaconsumer/pconsumer.py &

#start apache service
echo "[INFO] : Starting apache server"
apache2ctl -D "FOREGROUND"

