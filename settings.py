import external.autodeps as deps
import os.path
# Django settings for booking project.

PROJECT_PATH = os.path.abspath('%s' % os.path.dirname(__file__))

INTERNAL_IPS = ('127.0.0.1',)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('glibersat', 'glibersat@sigill.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Eupore/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

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
MEDIA_URL = 'http://localhost:8000/site_media/'

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
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'booking.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates/',
)

# For Django-autodeps
DEPENDENCY_ROOT = os.path.join(PROJECT_PATH, 'external')

DEPENDENCIES = (
    # SOUTH
    deps.HG('http://bitbucket.org/andrewgodwin/south/',
            revision='0.6.2',
            pathtomodule='south',
            root=DEPENDENCY_ROOT,
            ),

    # REGISTRATION
    deps.HG('http://bitbucket.org/ubernostrum/django-registration/',
             app_name='registration',
             pathtomodule='registration',
             root=DEPENDENCY_ROOT,
             ),

    # SCHEDULE
    deps.GIT('git://github.com/thauber/django-schedule.git',
             app_name='django-schedule',
             pathtomodule='django-schedule',
             root=DEPENDENCY_ROOT,
             ),

    # AUTHORITY
    deps.HG('http://bitbucket.org/jezdez/django-authority/',
            pathtomodule='django-authority/src/',
            root=DEPENDENCY_ROOT,
            ),

    # TAGGING
    deps.SVN('http://django-tagging.googlecode.com/svn/trunk/',
             app_name='django-tagging',
             pathtomodule='django-tagging',
             root=DEPENDENCY_ROOT,
             ),

    # Photologue
    deps.SVN('http://django-photologue.googlecode.com/svn/trunk',
             app_name='photologue',
             pathtomodule='photologue',
             root=DEPENDENCY_ROOT,
             ),

    # ImageKit
    deps.HG('http://bitbucket.org/jdriscoll/django-imagekit/',
            app_name='imagekit',
            pathtomodule='imagekit',
            root=DEPENDENCY_ROOT,
            ),

    # Reversion
    deps.SVN('http://django-reversion.googlecode.com/svn/tags/1.2/src/reversion',
             app_name='reversion',
             root=DEPENDENCY_ROOT,
             ),

    # Annoying
    deps.HG('http://bitbucket.org/offline/django-annoying/',
            app_name='annoying',
            pathtomodule='annoying',
            root=DEPENDENCY_ROOT,
            ),

    # SocialAuth
    deps.GIT('git://github.com/uswaretech/Django-Socialauth.git',
             app_name='socialauth',
             pathtomodule='socialauth',
             root=DEPENDENCY_ROOT,
             ),

    deps.GIT('git://github.com/flashingpumpkin/django-socialregistration.git',
             #revision='v0.2-dev',
             app_name='socialregistration',
             pathtomodule='socialregistration',
             root=DEPENDENCY_ROOT,
             ),

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

    # External
#    'debug_toolbar',
    'django_extensions',
    'south',
    'registration',
    'schedule',
    'authority',
    'tagging',
    'photologue',
    'reversion',
    'imagekit',
    'annoying',
    'socialregistration',

    # Internal
    'backcap',
    'account',
    'minisite',
    'minisite-portlets',
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


### Registration
ACCOUNT_ACTIVATION_DAYS = 7

### LOGIN
# General
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                           'socialregistration.auth.OpenIDAuth',
                           )

### PROFILES
AUTH_PROFILE_MODULE  = 'account.UserProfile'
