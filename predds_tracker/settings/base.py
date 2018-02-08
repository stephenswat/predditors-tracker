import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'predds_tracker',
    'eve_sde',
    'system_statistics',
    'django_cron',
    'tools',
    'debug_toolbar'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'predds_tracker.pipeline.get_username',
    'predds_tracker.pipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'predds_tracker.pipeline.create_alt',
    'predds_tracker.pipeline.reject_alliance',
)

CRON_CLASSES = [
    'system_statistics.cron.UpdateStatistics',
    'predds_tracker.cron.UpdateLocations',
]

ROOT_URLCONF = 'predds_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'predds_tracker.wsgi.application'
AUTH_USER_MODEL = 'predds_tracker.Character'
AUTHENTICATION_BACKENDS = ['predds_tracker.auth.CustomEVEOnlineOAuth2', 'django.contrib.auth.backends.ModelBackend']
SOCIAL_AUTH_EVEONLINE_SCOPE = []
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/eveonline/'

LANGUAGE_CODE = 'en-us'
DATETIME_FORMAT = 'F j, Y, H:i'

TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = False

STATIC_URL = '/static/'
INTERNAL_IPS = ['127.0.0.1']
