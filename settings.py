# Django settings for sunlightlabs project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
    ('James Turk', 'jturk@sunlightfoundation.com'),
    ('timball', 'timball@sunlightfoundation.com'),
)

CACHE_BACKEND = 'file:///home/james/code/sunlight/sunlightlabs/dbgcache'

MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

EMAIL_SUBJECT_PREFIX = '[sunlightlabs.com] '

TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
if DEBUG:
    ADMIN_MEDIA_PREFIX = '/media/admin/'
else:
    ADMIN_MEDIA_PREFIX = '***REMOVED***'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '***REMOVED***'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_openid.consumer.SessionConsumer',
    'gatekeeper.middleware.GatekeeperMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'sunlightlabs.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'debug_toolbar',
    'django_openid',
    'tagging',
    'mediasync',
    'feedinator',
    'gatekeeper',
    'blogdor',
    'simplesurvey',
    'newsfeed',
    'popular',
    'meritbadges',
    'sunlightlabs.labs',
    'sunlightlabs.appcontest',
    'sunlightlabs.appjudging',
    'anthill.people',
    'anthill.ideas',
    'anthill.projects',
    'anthill.events',
)

DATE_FORMAT = 'F j, Y'

AUTH_PROFILE_MODULE = 'people.Profile'

EMAIL_HOST = "smtp.sunlightlabs.com"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "***REMOVED***"
EMAIL_HOST_PASSWORD = "***REMOVED***"
EMAIL_USE_TLS = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

AWS_KEY = '***REMOVED***'
AWS_SECRET = '***REMOVED***'
AWS_BUCKET = 'assets.sunlightlabs.com'

MEDIASYNC_AWS_KEY = AWS_KEY
MEDIASYNC_AWS_SECRET = AWS_SECRET
MEDIASYNC_AWS_BUCKET = 'assets.sunlightlabs.com'
MEDIASYNC_AWS_PREFIX = 'site3'

BLOGDOR_NOTIFY_ON_COMMENT = True
BLOGDOR_ENABLE_FEEDS = False
#AKISMET_KEY = '54f2d2830563'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/people/%s/" % o.username
}

GATEKEEPER_MODERATOR_LIST = ['jcarbaugh@sunlightfoundation.com','cjohnson@sunlightfoundation.com',
                            'jturk@sunlightfoundation.com']

GRAVATAR_DEFAULT = "http://assets.sunlightlabs.com/site3/images/avatar.jpg"
GRAVATAR_SIZE = 60
FORCE_LOWERCASE_TAGS = True

GMAPS_API_KEY = '***REMOVED***'
GOOGLE_ANALYTICS_EMAIL = 'sunlightlabs@gmail.com'
GOOGLE_ANALYTICS_PASSWORD = '***REMOVED***'
GOOGLE_ANALYTICS_ID = '***REMOVED***'

SIMPLESURVEY_COMPLETE_REDIRECT = "/judgeforamerica/appsforamerica2/"

RESTRUCTUREDTEXT_FILTER_SETTINGS = {'initial_header_level': 3}
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ANTHILL_DEFAULT_MARKUP = 'markdown'

try:
    from local_settings import *
except ImportError, exp:
    pass
