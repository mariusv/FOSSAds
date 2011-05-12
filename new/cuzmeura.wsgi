import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'cuZmeura.settings'

sys.path.append('/var/www/html/cuZmeura')
sys.path.append('/var/www/html/')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()