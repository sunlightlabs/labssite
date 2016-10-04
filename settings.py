# Django settings for sunlightlabs project.
import os

from django.utils.html import urlize
import markdown
import markdown2

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

EMAIL_SUBJECT_PREFIX = '[sunlightlabs.com] '
DEFAULT_FROM_EMAIL = ''

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
    ADMIN_MEDIA_PREFIX = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'debug_toolbar',
    'haystack',
    'tagging',
    'mediasync',
    'blogdor',
    'labs',
    'anthill.projects',
    'markupwiki',
)

DATE_FORMAT = 'F j, Y'

EMAIL_HOST = ""
EMAIL_PORT = "25"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = ( PROJECT_ROOT + '/templates', )

AWS_KEY = ''
AWS_SECRET = ''
AWS_BUCKET = ''

MEDIASYNC_AWS_KEY = AWS_KEY
MEDIASYNC_AWS_SECRET = AWS_SECRET
MEDIASYNC_AWS_BUCKET = 'assets.sunlightlabs.com'
MEDIASYNC_AWS_PREFIX = 'site3.1'
MEDIASYNC_JS_PATH = 'scripts'
MEDIASYNC_CSS_PATH = 'styles'

BLOGDOR_ENABLE_FEEDS = False

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/blog/author/%s/" % o.username,
}

GRAVATAR_DEFAULT = "http://assets.sunlightlabs.com/site3.1/images/avatar.jpg"
GRAVATAR_SIZE = 60
FORCE_LOWERCASE_TAGS = True

ANTHILL_GMAPS_KEY = ''
GOOGLE_ANALYTICS_EMAIL = ''
GOOGLE_ANALYTICS_PASSWORD = ''
GOOGLE_ANALYTICS_ID = ''

RESTRUCTUREDTEXT_FILTER_SETTINGS = {'initial_header_level': 3}

ANTHILL_DEFAULT_MARKUP = 'markdown'

def custom_markdown(*args, **kwargs):
    kwargs['extras'] = ("footnotes",)
    return markdown2.markdown(*args, **kwargs)

MARKUP_FIELD_TYPES = (
    ('markdown', custom_markdown),
    ('html', lambda markup: markup),
    ('plain', lambda markup: urlize(linebreaks(markup))),
)

MARKUPWIKI_DEFAULT_MARKUP_TYPE = 'markdown'
MARKUPWIKI_MARKUP_TYPE_EDITABLE = False
MARKUPWIKI_EDITOR_TEST_FUNC = lambda u: u.is_staff

BLOGDOR_AUTHOR_GROUP = 'Bloggers'

HAYSTACK_SITECONF = 'labs.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = 'whoosh_index'

try:
    from local_settings import *
except ImportError, exp:
    pass
