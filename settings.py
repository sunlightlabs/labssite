# Django settings for sunlightlabs project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
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
if DEBUG:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = 'http://assets.sunlightlabs.com/site/'

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
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'gatekeeper.middleware.GatekeeperMiddleware',
)

ROOT_URLCONF = 'sunlightlabs.urls'

INSTALLED_APPS = (
	'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'tagging',
    'sunlightcore',
    'gatekeeper',
    'djitter',
    'blogdor',
    'showcase',
    'sunlightlabs.labs',
    'sunlightlabs.appcontest',
)

EMAIL_HOST = "smtp.sunlightlabs.com"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "***REMOVED***"
EMAIL_HOST_PASSWORD = "***REMOVED***"
EMAIL_USE_TLS = True

ALLOWED_TO_DM = ['cjoh','felskia','gregelin','jamesturk','jcarbaugh','jroo','timball']

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

AWS_KEY = '***REMOVED***'
AWS_SECRET = '***REMOVED***'
AWS_BUCKET = 'assets.sunlightlabs.com'

MEDIASYNC_AWS_KEY = AWS_KEY
MEDIASYNC_AWS_SECRET = AWS_SECRET
MEDIASYNC_AWS_BUCKET = 'assets.sunlightlabs.com'
MEDIASYNC_AWS_PREFIX = 'site'

TWITTER_USERNAME = 'sunlightlabs'

BLOGDOR_NOTIFY_ON_COMMENT = True
AKISMET_KEY = '54f2d2830563'

GATEKEEPER_MODERATOR_LIST = ['jcarbaugh@sunlightfoundation.com','cjohnson@sunlightfoundation.com']

GRAVATAR_DEFAULT = "http://assets.sunlightlabs.com/site/images/avatar_new.jpg"
GRAVATAR_SIZE = 60
FORCE_LOWERCASE_TAGS = True

try:
    from local_settings import *
except ImportError, exp:
    pass
