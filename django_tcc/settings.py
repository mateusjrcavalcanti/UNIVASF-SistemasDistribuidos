from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-$3%6573(6q7!spqw7=5_bka0^y34xx#9^-ji32g3v15azs2^oq'
DEBUG = True
ALLOWED_HOSTS = ["localhost"]


# Application definition

AUTH_USER_MODEL = 'tcc.User'

if 'CODESPACE_NAME' in os.environ:
    codespace_name = os.getenv("CODESPACE_NAME")
    codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    CSRF_TRUSTED_ORIGINS = [
        f'https://{codespace_name}-8000.{codespace_domain}']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_browser_reload",
    'tcc',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

X_FRAME_OPTIONS = "ALLOW-FROM preview.app.github.dev"

ROOT_URLCONF = 'django_tcc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "django_tcc" / "templates"],
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

WSGI_APPLICATION = 'django_tcc.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = False
USE_TZ = True
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


# Static files (CSS, JavaScript, Images)

USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'django_tcc', 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'django_tcc', 'static'),)

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'django_tcc', 'mediafiles')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin Template Jazzmin Settings

JAZZMIN_SETTINGS = {
    "site_title": "TCC Poject",
    "site_header": "TCC Poject",
    "site_brand": "TCC Poject",
    "welcome_sign": "Welcome to TCC Poject",
    "copyright": "Mateus Jr, Breno e Alan",

    "related_modal_active": True,

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",
        "tcc.curso": "fas fa-graduation-cap",
        "tcc.semestre": "fas fa-calendar-alt",
        "tcc.trabalho": "fas fa-book",
        "tcc.horario": "fas fa-clock",
        "tcc.banca": "fas fa-microphone",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "use_google_fonts_cdn": True,
    "show_ui_builder": True,

    "changeform_format_overrides": {"auth.user": "horizontal_tabs", "auth.group": "horizontal_tabs", "tcc.semestre": "horizontal_tabs"},

    "custom_links": {
        "auth": [{
            "name": "Users",
            "url": "/admin/tcc/user/",
            "icon": "fas fa-user",
            "permissions": ["tcc.view_user"]
        }]
    },
    "hide_models": ['tcc.user'],

}

# EMAIL SETTINGS
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # ADMIN EMAIL
ADMIN_EMAIL = env('ADMIN_EMAIL')
