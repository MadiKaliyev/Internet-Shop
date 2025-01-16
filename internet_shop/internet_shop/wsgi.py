import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/madi/project1/project1/internet_shop')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internet_shop.settings')

application = get_wsgi_application()
