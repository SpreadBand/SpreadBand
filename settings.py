# import external.autodeps as deps
import os.path
# Django settings for spreadband project.

PROJECT_PATH = os.path.abspath('%s' % os.path.dirname(__file__))

INTERNAL_IPS = ('127.0.0.1',)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('glibersat', 'glibersat@sigill.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'spreadband',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'spreadband',
        'PASSWORD': '',
        },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

_ = lambda s: s
LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k93k=6s8%hc5xg5l4pt%+#!6^wp=+elxmq4c9xf7j&$#a42col'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',

    # CSRF Attacks
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'reversion.middleware.RevisionMiddleware',


    # Request (stats)
    'request.middleware.RequestMiddleware',
    #'openid_consumer.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'spreadband.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates/',
)

INSTALLED_APPS = (
    # Built-in
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.localflavor',
    'django.contrib.syndication',
    'django.contrib.messages',

    # External
    'compressor',
    'debug_toolbar',
    'django_extensions',
    'south',
    'registration',
    'guardian',
    'tagging',
    'reversion',
    'imagekit',
    'annoying',
    'socialregistration',
    'voting',
    'agenda',
    'uni_form',
    'reviews',
    'profiles',
    'ajax_select',
    'actstream',
    'notification',
    'request',
    'threadedcomments',

    # Internal
    'backcap',
    'account',
    'minisite',
#    'minisite-portlets', <-- bug avec pgsql..
    'actors',
    'event',
    'band',
    'venue',
    'bargain',
    'album',

    'bigbrother',
)


###--- Application settings ---###

### DEBUG TOOLBAR
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False,
    }


### Mailer
# Write emails to console if in development mode
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

### Registration
ACCOUNT_ACTIVATION_DAYS = 7

### LOGIN, AUTHENTICATION
# General
LOGIN_URL = '/user/reg/classical/login'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'utils.auth.backends.CaseInsensitiveUsernameEmailBackend',
    'socialregistration.auth.OpenIDAuth',
    'guardian.backends.ObjectPermissionBackend',
    )

### PROFILES
AUTH_PROFILE_MODULE  = 'account.UserProfile'

### TAGGING
FORCE_LOWERCASE_TAGS = True

### REVIEWS
REVIEWS_SHOW_PREVIEW = True
REVIEWS_IS_MODERATED = False


### AUTOCOMPLETE
AJAX_LOOKUP_CHANNELS = {
    # the simplest case, pass a DICT with the model and field to search against :
    'band' : dict(model='band.Band', search_field='name'),
    'venue' : dict(model='venue.Venue', search_field='name'),
    # this generates a simple channel
    # specifying the model Track in the music app, and searching against the 'title' field

    # or write a custom search channel and specify that using a TUPLE
    # 'contact' : ('peoplez.lookups', 'ContactLookup'),
    # this specifies to look for the class `ContactLookup` in the `peoplez.lookups` module
}

### GUARDIAN
ANONYMOUS_USER_ID = -1

### COMMENTS
COMMENTS_APP = 'threadedcomments'
