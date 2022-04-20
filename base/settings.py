"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


import os
import django_heroku
import dj_database_url
from decouple import config, Csv
from django.contrib.messages import constants as messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'accounts',
    'category',
    'post',
    'search',
    # CKeditor
    'ckeditor_uploader',
    'ckeditor',
    # Tag
    'taggit',
    # MPTT
    'mptt',

    'tinymce',

    # Cloud
    'cloudinary_storage',
    'cloudinary',

    'django.contrib.sitemaps',

    'django.contrib.sites',
    'django.contrib.redirects',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',

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

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]


# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CKEDITOR_UPLOAD_PATH="uploads/"

TAGGIT_CASE_INSENSITIVE = True


TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    # "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "en",  # To force a specific language instead of the Django current language.
}



# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono-lisa',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
#             {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             {'name': 'forms',
#              'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
#                        'HiddenField']},
#             '/',
#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
#                        'Language']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert',
#              'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
#             '/',
#             {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#             {'name': 'about', 'items': ['About']},
#             '/',  # put this to force next toolbar on new line
#             {'name': 'yourcustomtools', 'items': [
#                 # put the name of your editor.ui.addButton here
#                 'Preview',
#                 'Maximize',

#             ]},
#         ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
#         'height': 291,
#         'width': '100%',
#         # 'filebrowserWindowHeight': 725,
#         # 'filebrowserWindowWidth': 940,
#         # 'toolbarCanCollapse': True,
#         # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
#         'tabSpaces': 4,
#         'extraPlugins': ','.join([
#             'uploadimage', # the upload image feature
#             # your extra plugins here
#             'div',
#             'autolink',
#             'autoembed',
#             'embedsemantic',
#             'autogrow',
#             # 'devtools',
#             'widget',
#             'lineutils',
#             'clipboard',
#             'dialog',
#             'dialogui',
#             'elementspath',
#             # 'a11yhelp, 
#             # 'about, 
#             # 'adobeair, 
#             # 'ajax, 
#             # 'autoembed, 
#             # 'autogrow, 
#             # 'autolink, 
#             # 'bbcode, 
#             # 'clipboard, 
#             # 'codesnippet,
#             'codesnippetgeshi', 
#             'colordialog', 
#             'devtools', 
#             'dialog', 
#             'div', 
#             'divarea', 
#             'docprops', 
#             'embed', 
#             'embedbase',
#             'embedsemantic', 
#             'filetools', 
#             'find', 
#             # 'flash', 
#             'forms', 
#             'iframe', 
#             'iframedialog', 
#             'image', 
#             'image2', 
#             'language',
#             'lineutils', 
#             'link', 
#             'liststyle', 
#             'magicline', 
#             'mathjax', 
#             'menubutton', 
#             'notification', 
#             'notificationaggregator',
# # pagebreak, pastefromword, placeholder, preview, scayt, sharedspace, showblocks, smiley,
# # sourcedialog, specialchar, stylesheetparser, table, tableresize, tabletools, templates, uicolor,
# # uploadimage, uploadwidget, widget, wsc, xml
#         ]),
#     }
# }

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': 'Full',
        'toolbar_YourCustomToolbarConfig': 'Full',
        'toolbar': 'Full',  # put selected toolbar config here
        'toolbarGroups': 'Full',
        'height': 291,
        'width': '102%',
    }
}

# from ckeditor.configs import DEFAULT_CONFIG  # noqa

# CUSTOM_TOOLBAR = [
#     {
#         "name": "document",
#         "items": [
#             "Styles",
#             "Format",
#             "Bold",
#             "Italic",
#             "Underline",
#             "Strike",
#             "-",
#             "TextColor",
#             "BGColor",
#             "-",
#             "JustifyLeft",
#             "JustifyCenter",
#             "JustifyRight",
#             "JustifyBlock",
#         ],
#     },
#     {
#         "name": "widgets",
#         "items": [
#             "Undo",
#             "Redo",
#             "-",
#             "NumberedList",
#             "BulletedList",
#             "-",
#             "Outdent",
#             "Indent",
#             "-",
#             "Link",
#             "Unlink",
#             "-",
#             "Image",
#             "CodeSnippet",
#             "Table",
#             "HorizontalRule",
#             "Smiley",
#             "SpecialChar",
#             "-",
#             "Blockquote",
#             "-",
#             "ShowBlocks",
#             "Maximize",
#         ],
#     },
# ]
# CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_IMAGE_BACKEND = "ckeditor_uploader.backends.PillowBackend"
# CKEDITOR_THUMBNAIL_SIZE = (300, 300)
# CKEDITOR_IMAGE_QUALITY = 40
# CKEDITOR_BROWSE_SHOW_DIRS = True
# CKEDITOR_ALLOW_NONIMAGE_FILES = True

# CKEDITOR_CONFIGS = {
#     "default": DEFAULT_CONFIG,
#     "my-custom-toolbar": {
#         "skin": "moono-lisa",
#         "toolbar": CUSTOM_TOOLBAR,
#         "toolbarGroups": None,
#         "extraPlugins": ",".join(["image2", "codesnippet", "timestamp"]),
#         "removePlugins": ",".join(["image"]),
#         "codeSnippet_theme": "xcode",
#     },
# }


LOGIN_URL = '/accounts/login/'

USERNAME_FIELD = 'email'
REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


AUTH_USER_MODEL = 'accounts.Account'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Activate Django-Heroku.
django_heroku.settings(locals())

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
CLOUDINARY_URL = config('CLOUDINARY_URL')

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = True

CSRF_TRUSTED_ORIGINS = [config('CSRF_TRUSTED_ORIGINS')]

CSRF_COOKIE_DOMAIN = config('CSRF_COOKIE_DOMAIN')

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())