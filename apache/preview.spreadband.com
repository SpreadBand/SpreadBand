<VirtualHost *:80>
    ServerName preview.spreadband.com

    WSGIDaemonProcess www-data
    WSGIProcessGroup www-data
 
    WSGIScriptAlias / /home/spreadband/virtualenvs/preview.spreadband.com/spreadband/apache/production.wsgi/
 
    <Location "/">
        Order Allow,Deny
        Allow from all
    </Location>
 

    <Directory /home/spreadband/virtualenvs/preview.spreadband.com/spreadband/media>
        Options -Indexes FollowSymLinks
    </Directory>

    <Location "/site_media">
        SetHandler None
    </Location>
 
    Alias /site_media /home/spreadband/virtualenvs/preview.spreadband.com/spreadband/media
 
    <Location "/media">
        SetHandler None
        Options -Indexes FollowSymLinks
    </Location>
 
    Alias /media /home/spreadband/virtualenvs/preview.spreadband.com/lib/python2.5/site-packages/django/contrib/admin/media/

    ErrorLog /home/spreadband/logs/error.log
    LogLevel info
    CustomLog /home/spreadband/logs/access.log combined
</VirtualHost>

