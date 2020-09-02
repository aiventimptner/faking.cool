import os

from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon.settings.production')

application = get_asgi_application()
