import os
from predds_tracker.settings.base import *


SECRET_KEY = 'predds'
DEBUG = True
ALLOWED_HOSTS = []

SOCIAL_AUTH_EVEONLINE_KEY = '12a8108579a74bb79e51d1af0ca8edd9'
SOCIAL_AUTH_EVEONLINE_SECRET = 'IC25410g12zKIgW7Zzfy6rVFW9hwy29tBqAoEmGD'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
