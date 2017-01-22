import os
from predds_tracker.settings.base import *

SECRET_KEY = 'YOUR STUFF GOES HERE'
DEBUG = True
ALLOWED_HOSTS = []

SOCIAL_AUTH_EVEONLINE_KEY = 'YOUR STUFF GOES HERE'
SOCIAL_AUTH_EVEONLINE_SECRET = 'YOUR STUFF GOES HERE'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
