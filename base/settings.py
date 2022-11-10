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


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'category',
    'post',
    "users",
    # CKeditor
    'ckeditor_uploader',
    'ckeditor',
    # Tag
    'taggit',

    # Cloud
    'cloudinary_storage',
    'cloudinary',

    'django.contrib.sitemaps',
    'pwa',
    "django.contrib.sites",
    "django_comments_ink",
    "django_comments",
    'django_social_share',
]

SITE_ID = int(os.getenv('SITE_ID'))

PREPEND_WWW = os.getenv('PREPEND_WWW', default=False)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise
    'django.middleware.locale.LocaleMiddleware', # locale
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


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
				'post.context_processors.sidebar',
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
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)


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


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Youtube', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['CodeSnippet']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'Custom',  # put selected toolbar config here
        'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 500,
        'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.7-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'a11yhelp', 
            'about', 
            'adobeair', 
            'ajax', 
            'codesnippet',
            # 'codesnippetgeshi', 
            'colordialog', 
            'divarea', 
            'docprops', 
            'embed', 
            'embedbase',
            'filetools', 
            'find', 
            'forms', 
            'iframe', 
            'iframedialog', 
            'image', 
            'language',
            'link', 
            'liststyle', 
            'magicline', 
            'mathjax', 
            'menubutton', 
            'notification', 
            'notificationaggregator',
            'pagebreak',
            'pastefromword', 
            'placeholder', 
            'preview', 
            'scayt', 
            'sharedspace', 
            'showblocks', 
            'smiley',
            'sourcedialog', 
            'specialchar', 
            'stylesheetparser', 
            'table', 
            'tableresize', 
            'tabletools', 
            'templates', 
            'uicolor',
            'uploadwidget', 
            'widget', 
            'wsc', 
            'xml'
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
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = True


CSRF_TRUSTED_ORIGINS = [os.getenv('CSRF_TRUSTED_ORIGINS')]

CSRF_COOKIE_DOMAIN = os.getenv('CSRF_COOKIE_DOMAIN')

CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST')

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'templates/pwa', 'serviceworker.js')

PWA_APP_NAME = 'HOANG VAN GIOI'
PWA_APP_DESCRIPTION = "My blog web app "
PWA_APP_THEME_COLOR = '#ec3fce'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

PWA_APP_ICONS = [
    {
        'src': '/static/images/icons/icon-72x72.png',
        'size': '72x72',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-96x96.png',
        'size': '96x96',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-128x128.png',
        'size': '128x128',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        'size': '144x144',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-152x152.png',
        'size': '152x152',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-192x192.png',
        'size': '192x192',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-384x384.png',
        'size': '384x384',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        'size': '512x512',
        'type': 'image/png',
        'purpose': 'maskable'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/icons/icon-72x72.png',
        'size': '72x72',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-96x96.png',
        'size': '96x96',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-128x128.png',
        'size': '128x128',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        'size': '144x144',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-152x152.png',
        'size': '152x152',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-192x192.png',
        'size': '192x192',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-384x384.png',
        'size': '384x384',
        'type': 'image/png',
        'purpose': 'maskable'
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        'size': '512x512',
        'type': 'image/png',
        'purpose': 'maskable'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-750x1334.png',
        'media': '(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-1242x2208.png',
        'media': '(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/static/images/icons/splash-1125x2436.png',
        'media': '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/static/images/icons/splash-828x1792.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-1242x2688.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)'
    },
    {
        'src': '/static/images/icons/splash-1536x2048.png',
        'media': '(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-1668x2224.png',
        'media': '(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-1668x2388.png',
        'media': '(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)'
    },
    {
        'src': '/static/images/icons/splash-2048x2732.png',
        'media': '(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'vi-VN'

# Define the user model. The difference between 'users.User' and 'auth.User'
AUTH_USER_MODEL = "users.User"

SIGNUP_URL = "/user/signup/"
LOGIN_URL = "/user/login/"
LOGOUT_URL = "/user/logout/"
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
    "post.post": 10  # So 2 levels: from 0 to 1.
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
    "post.post": {
        "check_input_allowed": "post.models.check_comments_input_allowed"
    },
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

# COMMENTS_INK_THEME_DIR = "feedback_in_header"


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
