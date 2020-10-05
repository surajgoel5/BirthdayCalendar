"""
WSGI config for bdayCal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import multiprocessing
import threading


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bdayCal.settings')

application = get_wsgi_application()



#from mailer.apps import mailerFunc #.func as func
#threading.Thread(target=mailerFunc).start()
