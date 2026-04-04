"""
WSGI config for marketplace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

# Add the backend directory to sys.path so Vercel can find the 'marketplace' and 'api' modules
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

application = get_wsgi_application()

# Required by Vercel
app = application

# Required by Vercel
app = application
