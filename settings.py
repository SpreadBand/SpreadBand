# -*- coding: utf-8 -*-
# Django settings for spreadband project.

import os.path

DEFAULT_CHARSET = 'utf-8'

PROJECT_PATH = os.path.abspath('%s' % os.path.dirname(__file__))

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Guillaume Libersat', 'guillaume@spreadband.com'),
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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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

# For numerical stuff
USE_L10N = True

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
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'announcements.context_processors.site_wide_announcements',
    'backcap.context_processors.backcap_forms',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # I18N
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',

    # CSRF Attacks
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # For CBV, remove before upgrading to 1.3
    'cbv.middleware.DeferredRenderingMiddleware',

    # reversion
    'reversion.middleware.RevisionMiddleware',

    # Facebook
    #'socialregistration.middleware.FacebookMiddleware',

    # Request (stats)
    'request.middleware.RequestMiddleware',
    #'openid_consumer.middleware.OpenIDMiddleware',

    # Flatpages
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # 403
    'utils.middleware.403.Django403Middleware',

    # Locale for user
    'userena.middleware.UserenaLocaleMiddleware',

    # Redirects
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'spreadband.urls'

if DEBUG:
    TEMPLATE_DIRS = ('templates/',)
else:
    TEMPLATE_DIRS = ('/home/spreadband/virtualenvs/spreadband.com/spreadband/templates/',)

INSTALLED_APPS = (
    'south',
    'lettuce.django',

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
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.redirects',

    # Internal
    'sb_base',
    'world',
    'media',
    # 'minisite',
#    'minisite-portlets', <-- bug avec pgsql..
    'actors',
    'event',
    'band',
    'presskit',
    'venue',
    'album',
    # 'gigbargain',
    # 'bigbrother',
    # 'api',
    'account',
    'haystack',

    # External
    'userena',
    'oauth_access',
    'dajaxice',
    'dajax',
    'django_static',
    'debug_toolbar',
    'django_extensions',
    'django_nose',
    'registration',
    'profiles',
    'guardian',
    'timedelta',
    'tagging',
    'reversion',
    'imagekit',
    'annoying',
    'socialregistration',
    'voting',
    'agenda',
    'uni_form',
    'reviews',
    'ajax_select',
    'actstream',
    'notification',
    'request',
    'threadedcomments',
    'django_fsm',
    'elsewhere',
    'timezones',
    'django_countries',
    'mailer',
    'oembed',
    'robots',
    'faq',
    'django_wysiwyg',
    'avatar',
    'announcements',
    'backcap',
    'django_filters',
    'contacts_import',
    'socialbridge',
    'template_utils',
    'visitors',
    'badges',
    'cbv',
    'chronograph',
)

if DEBUG:
    INSTALLED_APPS += (
            'rosetta',
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
    'EXTRA_SIGNALS': ['gigbargain.signals.gigbargain_concluded']
    }


### Mailer
SERVER_EMAIL = 'noreply@spreadband.com'
EMAIL_SENDER = SERVER_EMAIL
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = '[SpreadBand] '
# Write emails to console if in development mode
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else, use SMTP
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25

MAILER_EMAIL_BACKEND = EMAIL_BACKEND


### Registration
ACCOUNT_ACTIVATION_DAYS = 7

### LOGIN, AUTHENTICATION
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
#    'utils.auth.backends.CaseInsensitiveUsernameEmailBackend',
    'guardian.backends.ObjectPermissionBackend',
    )

LOGIN_URL = '/user/signin/'

### USERENA
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_DISABLE_PROFILE_LIST = True
LOGIN_REDIRECT_URL = USERENA_SIGNIN_REDIRECT_URL

### PROFILES
AUTH_PROFILE_MODULE  = 'account.UserProfile'

### TAGGING
FORCE_LOWERCASE_TAGS = True

### REVIEWS
REVIEWS_SHOW_PREVIEW = True
REVIEWS_IS_MODERATED = False

### COUNTRIES
COUNTRIES_FLAG_URL = 'images/flags/%(code)s.png'

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
PROFANITIES_LIST = ()

### API KEYS
# GOOGLE MAPS
GOOGLE_MAPS_API_KEY = 'ABQIAAAA6h516tSP1Hvn-DSlCn0BohSzw_xTdwUeZJiiJ-EpCmf90rYO0xT--Tl2YeDvj8A_LzJZPUdaTSawsQ'

# TWITTER (SpreadBand app)
TWITTER_CONSUMER_KEY = 'JyyMnvo7ziWIepALdanhMg'
TWITTER_CONSUMER_SECRET_KEY = 'N7wx9w1UJUNM0h8vVH6wB2vUIAiFYnO2p0IdAYtK2HE'
TWITTER_REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
TWITTER_AUTHORIZATION_URL = 'https://twitter.com/oauth/authorize'

# FACEBOOK
FACEBOOK_API_KEY = '0445acaf091af7727ef610e64cb73baf'
FACEBOOK_SECRET_KEY = '52f03de8cc57d0435eb1fcf8ba54a24e'

# OAUTH
OAUTH_ACCESS_SETTINGS = {
    'twitter': {
        'keys': {
            'KEY': TWITTER_CONSUMER_KEY,
            'SECRET': TWITTER_CONSUMER_SECRET_KEY,
            },
        'endpoints': {
            'access_token': TWITTER_ACCESS_TOKEN_URL,
            'request_token': TWITTER_REQUEST_TOKEN_URL,
            'authorize': TWITTER_AUTHORIZATION_URL,
            'callback': 'account.views.oauth_access_success',
            }
        },
    'facebook': {
        'keys': {
            'KEY': FACEBOOK_API_KEY,
            'SECRET': FACEBOOK_SECRET_KEY,
            },
        'endpoints': {
            'provider_scope': ('publish_stream', 'create_event', 'offline_access'),
            'access_token': 'https://graph.facebook.com/oauth/access_token',
            'authorize': 'https://graph.facebook.com/oauth/authorize',
            'callback': 'account.views.oauth_access_success',
            }
        }
    }

### HAYSTACK
HAYSTACK_SITECONF = 'spreadband.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, 'spreadband_index')

# STATIC FILES
DJANGO_STATIC = True
DJANGO_STATIC_MEDIA_URL = MEDIA_URL
#if not DEBUG:
# DJANGO_STATIC_SAVE_PREFIX = "/tmp/sb-media-cache"

# ROSETTA
if DEBUG:
    ROSETTA_WSGI_AUTO_RELOAD = True

# WYSIWYG editors
DJANGO_WYSIWYG_FLAVOR = "ckeditor"

# DAJAX(ICE)
DAJAXICE_MEDIA_PREFIX = "js/dajax"
DAJAXICE_XMLHTTPREQUEST_JS_IMPORT = True
DAJAXICE_JSON2_JS_IMPORT = True
DAJAXICE_DEBUG = DEBUG

# DJANGO AVATAR
AVATAR_DEFAULT_SIZE = 80
AVATAR_CROP_VIEW_SIZE = 450
AVATAR_MAX_AVATARS_PER_USER = 10
AVATAR_HASH_FILENAMES = True
AUTO_GENERATE_AVATAR_SIZES = (80, 48, 36, 30, 18)
AVATAR_GRAVATAR_DEFAULT = 'monsterid'

# CONTACTS IMPORT
CONTACTS_IMPORT_CALLBACK = 'account.views.contacts'

# SUPERLAURENT's email
VENUE_CANTFIND_EMAIL = 'laurent@spreadband.com'

# BADGES
BADGE_LEVEL_CHOICES = (
    ('P', "PressKit completed"),
)

# REQUESTS (ANALYTICS)
REQUEST_IGNORE_PATHS = (
    r'^admin/',
)

REQUEST_IGNORE_USERNAME = (
    'Laurent',
    'glibersat',
    )

REQUEST_TRAFFIC_MODULES = (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.Hit',
    'request.traffic.Error',
    'request.traffic.Search',
    'request.traffic.UniqueUser',
    'request.traffic.User',
)

# ELSEWHERE
ELSEWHERE_MEDIA_DIR = 'images/elsewhere/'
ELSEWHERE_ICON_PACK = ''
