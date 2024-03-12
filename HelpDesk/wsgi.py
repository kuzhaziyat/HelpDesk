import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/srv/www/serviceDesk/HelpDesk/venv/lib/python3.12/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelpDesk.settings')

application = get_wsgi_application()