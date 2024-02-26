import os, sys
from django.core.wsgi import get_wsgi_application

# project_path = '/Users/jang-youngjoon/dev-projects/break-server'
project_path = '/home/ubuntu/docker-server/break-server'

sys.path.append(project_path)
sys.path.append(os.path.join(project_path, 'venv/lib/python3.9/site-packages'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "breakserver.settings.production")

application = get_wsgi_application()
