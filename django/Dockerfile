FROM python:3

EXPOSE 80:80 8082:8082

#Copy setup required data
COPY scripts /root/scripts

#Copy application source to temporary location
COPY src /root/src

#Install required packages
#NOTE : Bestpractice says that mariadb database should be installed in separate container but
#       here for sake of simplicety we put everything in one container
RUN export DEBIAN_FRONTEND=noninteractive                                                        \
    && apt-get update                                                                            \
    && apt-get -y install apt-utils apache2 apache2-doc apache2-utils apache2-dev libapache2-mod-wsgi-py3  \
                  lynx libwww-perl libdbi-perl libdbd-mysql-perl libgd-gd2-perl vim net-tools    \
                  cron mariadb-server netcat                                                     \
    && /usr/local/bin/python -m pip install --upgrade pip                          \
    && pip install --no-cache-dir -r /root/scripts/requirements.txt                \
    && pip install --no-cache-dir --upgrade pymongo                                \
    && pip install mod_wsgi                                                        \
    && chmod +x /root/scripts/*.sh                                                 \
    && cat /root/scripts/apache2.conf > /etc/apache2/apache2.conf                  \
    && cat /root/scripts/tester.conf  > /etc/apache2/sites-available/tester.conf   \
    && echo 'LoadModule wsgi_module "/usr/local/lib/python3.8/site-packages/mod_wsgi/server/mod_wsgi-py38.cpython-38-x86_64-linux-gnu.so"' > /etc/apache2/mods-available/wsgi.load \
    && echo 'WSGIPythonHome "/usr/local"' >> /etc/apache2/mods-available/wsgi.load \
    && a2dissite 000-default.conf && a2ensite tester                               

#Create django infrastrucure and deploy applications code
RUN mkdir -p /opt/django && cd /opt/django                                         \
    && django-admin startproject challengetask                                     \ 
    && mv challengetask src && cd src                                              \ 
    && /opt/django/src/manage.py startapp pikaconsumer                             \
    && ./manage.py startapp dataholder                                             \
    && mv -f /root/src/challengetask/*.py /opt/django/src/challengetask            \
    && mv -f /root/src/dataholder/api  /opt/django/src/dataholder                  \
    && mv -f /root/src/dataholder/*.py /opt/django/src/dataholder                  \
    && mv -f /root/src/pikaconsumer/*.py /opt/django/src/pikaconsumer              \
    && chown -R www-data:www-data /opt/django/src                                  \
    && chmod -R 755 /opt/django/src


#Set login point to django work dir
WORKDIR /opt/django

