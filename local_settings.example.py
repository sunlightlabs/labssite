DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
    }
}

HAYSTACK_WHOOSH_PATH = '/projects/labssite/data/whoosh_index'
