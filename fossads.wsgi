import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'FOSSAds.settings'

sys.path.append('/var/www/html/FOSSAds')
sys.path.append('/var/www/html/')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
