import os
from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(str(BASE_DIR.joinpath('.env')))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # local
    'users.apps.UsersConfig',
    'deals.apps.DealsConfig',
    'products.apps.ProductsConfig',
    # 'accounts.apps.AccountsConfig',
    # third party
    'admin_honeypot',
    'django_filters',
    'bootstrap4',  # TODO: Override forms with raw BS and delete this lib
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    'djmoney',
    'django_quill',
    'debug_toolbar',
]

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'placeholder': 'Wspaniały opis okazji...',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                ],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                [{'list': ['ordered', 'bullet', ]}],
                ['link'],
                ['clean'],
            ]
        }
    }
}

CURRENCIES = ('USD', 'EUR', 'PLN')
CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('PLN', 'zł')]

SITE_ID = 1
LOGIN_REDIRECT_URL = 'deals:list'
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/profile/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ["127.0.0.1", ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
