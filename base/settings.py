"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


import os
import dj_database_url
import django_on_heroku
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
from distutils.util import strtobool
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', default='127.0.0.1')]

INTERNAL_IPS = ["127.0.0.1"]

ADMINS = ((os.getenv('NAME_ADMIN'), os.getenv('EMAIL_ADMIN')),)


CSRF_FAILURE_VIEW = 'base.views.handler403'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'category',
    'articles',
    "users",
    'contact',
    'pwa',
    # CKeditor
    'ckeditor_uploader',
    'ckeditor',
    # Tag
    'taggit',

    # Cloud
    'cloudinary_storage',
    'cloudinary',

    'django.contrib.sitemaps',
    "django.contrib.sites",
    "django_comments_ink",
    "django_comments",
    'corsheaders',
]

SITE_ID = int(os.getenv('SITE_ID'))

PREPEND_WWW = os.getenv('PREPEND_WWW', default=False)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise
    'django.middleware.locale.LocaleMiddleware', # locale
    'django.middleware.cache.UpdateCacheMiddleware', # cache
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # cache
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'base.middleware.RestrictStaffToAdminMiddleware',
    'base.middleware.MaintenanceModeMiddleware',
    'csp.middleware.CSPMiddleware',
]


MAINTENANCE_MODE = int(os.getenv("MAINTENANCE_MODE", 0))

MAINTENANCE_BYPASS_QUERY = os.getenv("MAINTENANCE_BYPASS_QUERY")

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
				'category.context_processors.category_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
        }
    }
else:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CKEDITOR_UPLOAD_PATH="uploads/"

TAGGIT_CASE_INSENSITIVE = True

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'

API_KEY_IFRAME = os.getenv('API_KEY_IFRAME')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'skin': 'theme',
        'width': 'auto',
        'allowedContent': True,
        'toolbarCanCollapse': True,
        'tabSpaces': 4,
        'mathJaxLib' : '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
        'mathJaxClass' : 'my-math',
        'embed_provider' : '//iframe.ly/api/oembed?url={{url}}&callback={{callback}}&api_key={}'.format(API_KEY_IFRAME),
        'magicline_everywhere' : True,
        'magicline_tabuList' : [ 'data-tabu' ],
        'magicline_color' : '#0000FF',
	    'uiColor' : '#AADC6E',
        'removePlugins': 'sourcearea',
        'qtCellPadding': '0',
        'qtCellSpacing': '0',
        'qtPreviewBackground': '#e36ef4',
        'extraPlugins': ','.join([
            # your extra plugins here
            'uploadimage', # the upload image feature
            'placeholder', 
            'uicolor',
            'devtools', 
            'ajax',
            'codesnippet', 
            'mathjax', 
            'embed', 
            'sourcedialog',
            'autoembed',
            'docprops', # Documennt project
            'magicline', 
            'quicktable',
        ]),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Activate Django-Heroku.
django_on_heroku.settings(locals(), logging=False)

MESSAGE_TAGS = {
    messages.DEBUG: 'text-blue-400',
    messages.INFO: 'text-blue-400',
    messages.SUCCESS: 'text-green-600',
    messages.WARNING: 'text-yellow-500',
    messages.ERROR: 'text-red-600',
}

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 10000

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 10000

options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)


CSRF_TRUSTED_ORIGINS = [os.getenv('CSRF_TRUSTED_ORIGINS')]

CSRF_COOKIE_DOMAIN = os.getenv('CSRF_COOKIE_DOMAIN')

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', None).split(',')

# SSL
SESSION_COOKIE_SECURE = bool(strtobool(os.getenv('SESSION_COOKIE_SECURE', 'True')))
CSRF_COOKIE_SECURE = bool(strtobool(os.getenv('CSRF_COOKIE_SECURE', 'True')))
SECURE_SSL_REDIRECT = bool(strtobool(os.getenv('SECURE_SSL_REDIRECT', 'True')))
LANGUAGE_COOKIE_HTTPONLY = bool(strtobool(os.getenv('LANGUAGE_COOKIE_HTTPONLY', 'True')))
SESSION_COOKIE_HTTPONLY = bool(strtobool(os.getenv('SESSION_COOKIE_HTTPONLY', 'True')))
CSRF_COOKIE_HTTPONLY = bool(strtobool(os.getenv('CSRF_COOKIE_HTTPONLY', 'True')))
SECURE_HSTS_PRELOAD = bool(strtobool(os.getenv('SECURE_HSTS_PRELOAD', 'True')))
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(strtobool(os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True')))
SECURE_BROWSER_XSS_FILTER = bool(strtobool(os.getenv('SECURE_BROWSER_XSS_FILTER', 'True')))
SECURE_CONTENT_TYPE_NOSNIFF = bool(strtobool(os.getenv('SECURE_CONTENT_TYPE_NOSNIFF', 'True')))

# Define the user model. The difference between 'users.User' and 'auth.User'
AUTH_USER_MODEL = "users.User"

SUPERUSER_NAME = os.getenv("SUPERUSER_NAME")
SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")

SIGNUP_URL = "/signup/"
LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

COMMENTS_APP = "django_comments_ink"

COMMENTS_HIDE_REMOVED = False

COMMENTS_INK_SALT = os.getenv("COMMENTS_INK_SALT", "").encode("utf-8")
COMMENTS_INK_CONFIRM_EMAIL = True  # Set to False to disable confirmation.
COMMENTS_INK_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
COMMENTS_INK_CONTACT_EMAIL = os.getenv('EMAIL_HOST_USER')

# Default to True, use False to allow other
# backend (say Celery based) send your emails.
COMMENTS_INK_THREADED_EMAILS = False

COMMENTS_INK_API_USER_REPR = lambda user: user.name

COMMENTS_INK_SEND_HTML_EMAIL = True

# This setting is to apply a maximum thread level of 1 to all apps by default.
COMMENTS_INK_MAX_THREAD_LEVEL = 1

# This setting applies a maximum thread level of 1 only to the 'quotes.quote'
# app model. Useful in case you want to allow different levels of comment
# nesting to different app models.
COMMENTS_INK_MAX_THREAD_LEVEL_BY_APP_MODEL = {
    "article.articles": 10  # So 2 levels: from 0 to 1.
}

COMMENTS_INK_LIST_ORDER = ("-thread__score", "thread__id", "order")

COMMENTS_INK_APP_MODEL_OPTIONS = {
    "default": {
        "who_can_post": "all",  # Valid values: "users", "all".
        "comment_flagging_enabled": True,
        "comment_votes_enabled": True,
        "comment_reactions_enabled": True,
        "object_reactions_enabled": True,
    },
    "article.articles": {
        "check_input_allowed": "articles.models.check_comments_input_allowed"
    }
}

COMMENTS_INK_CACHE_NAME = "default"

# All HTML elements rendered by django-comments-ink use the 'dci' CSS selector,
# defined in 'django_comments_ink/static/django_comments_ink/css/comments.css'.
# You can alter the CSS rules applied to your comments adding your own custom
# selector to the following setting.
# COMMENTS_INK_CSS_CUSTOM_SELECTOR = "dci dci-custom"

# How many users are listed when hovering a reaction.
COMMENTS_INK_MAX_USERS_IN_TOOLTIP = 10

# Display up to the given number of comments in the last page to avoid
# creating another page containing only these amount of comments.
COMMENTS_INK_MAX_LAST_PAGE_ORPHANS = 4

# Number of comments per page. When <=0 pagination is disabled.
COMMENTS_INK_COMMENTS_PER_PAGE = 10

COMMENTS_INK_THEME_DIR = "feedback_in_header"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(asctime)s %(module)s %(message)s"
        },
        "console": {
            "format": (
                "[%(asctime)s][%(levelname)s] %(name)s "
                "%(filename)s:%(funcName)s:%(lineno)d | %(message)s"
            ),
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'warning.log',
            'level': 'DEBUG',
            'formatter': 'console'
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        },
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django_comments_ink": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('MEMCACHED_HOSTS'),
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 1 # Để xác định bộ nhớ cache hết hạn 


PWA_APP_NAME = 'Hoan Van Gioi'
PWA_APP_DESCRIPTION = "My log web app"
PWA_APP_THEME_COLOR = '#e3e3ee'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '.'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

PWA_APP_ICONS = [
    {
        "src": "favicon.ico",
        "sizes": "64x64",
        "type": "image/x-icon",
        "purpose": "maskable any"
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "maskable any"
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        "sizes": "144x144",
        "type": "image/png",
        "purpose": "maskable any"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "favicon.ico",
        "sizes": "64x64",
        "type": "image/x-icon",
        "purpose": "maskable any"
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "maskable any"
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        "sizes": "144x144",
        "type": "image/png",
        "purpose": "maskable any"
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'templates/serviceworker.js')


PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'vi-VN'


# default source as self
CSP_DEFAULT_SRC = ("'self'", )

# style from our domain and bootstrapcdn
CSP_STYLE_SRC = ("'self'", )

# scripts from our domain and other domains
CSP_SCRIPT_SRC = ("'self'",
	"ajax.cloudflare.com",
	"static.cloudflareinsights.com",
	"google-analytics.com",
	"ssl.google-analytics.com",
	"googletagservices.com",
	"pagead2.googlesyndication.com",
    "partner.googleadservices.com",
    "adservice.google.com.vn",
    "adservice.google.com",
    "tpc.googlesyndication.com", 
)

# images from our domain and other domains
CSP_IMG_SRC = ("'self'",
	"res.cloudinary.com",
	"google-analytics.com",
    "pagead2.googlesyndication.com",
	"googleads.g.doubleclick.net")

# loading manifest, workers, frames, etc
CSP_FONT_SRC = ("'self'", )
CSP_CONNECT_SRC = ("'self'",
    "google-analytics.com",
    "pagead2.googlesyndication.com", 
    "partner.googleadservices.com",
    "adservice.google.com.vn", )

CSP_OBJECT_SRC = ("'self'", )
CSP_BASE_URI = ("'self'", )
CSP_FRAME_ANCESTORS = ("'self'", )
CSP_FORM_ACTION = ("'self'", )
CSP_INCLUDE_NONCE_IN = ('script-src', )
CSP_MANIFEST_SRC = ("'self'", )
CSP_WORKER_SRC = ("'self'", )
CSP_MEDIA_SRC = ("'self'", "res.cloudinary.com")
CSP_FRAME_SRC = ("'self'", 
    "googleads.g.doubleclick.net", 
    "tpc.googlesyndication.com", 
    "www.google.com", 
)


PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}


try:
    from .local_settings import *
except ImportError:
    pass