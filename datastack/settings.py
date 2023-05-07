from pathlib import Path
import dotenv
import datetime
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# accessing .env file from dir
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# DJANGO SECRET KEY
SECRET_KEY = os.environ["SECRET_KEY"]


# ALLOWED HOSTS & CORS & DEBUG
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
CORS_ORIGIN_ALLOW_ALL = os.environ["CORS_ORIGIN_ALLOW_ALL"] in ["True"]
DEBUG = os.environ["DEBUG"] in ["True"]


# INSTALLED APPS DEFAULT/USER
INSTALLED_APPS = [
    # Built-in apps
    "admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Dev Created Apps
    "datastack",
    "account",
    "category",
    "combo",
    "subscription",
    "users",
    "faq",
    "announcement",
    "maintenance",
    "social_media",
    "invoice",
    "helper",
    "cron",
    "privacy_policy",
    "tos",
    "webhook",

    # Dependency(installed) Apps
    "rest_framework",
    "django_crontab",
    "rest_framework_jwt",
    "corsheaders",
]


# MIDDLEWARE LAYERS
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# PASSWORD HASHERS
PASSWORD_HASHERS = ["django.contrib.auth.hashers.PBKDF2PasswordHasher"]


# DOMAIN NAMES
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
API_DOMAIN_NAME = os.environ["API_DOMAIN_NAME"]
DASHBOARD_DOMAIN_NAME = os.environ["DASHBOARD_DOMAIN_NAME"]


# AUTH USER MODEL
AUTH_USER_MODEL = os.environ["AUTH_USER_MODEL"]


# ROOT URL
ROOT_URLCONF = os.environ["ROOT_URLCONF"]


# WSGI APPLICATION
WSGI_APPLICATION = os.environ["WSGI_APPLICATION"]


# DEFAULT AUTH TOKEN CLASS
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (os.environ["JWT_AUTH_TOKEN_CLASS"],)
}


# JWT AUTH TOKENS & SECRETS
JWT_AUTH = {
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(
        minutes=int(os.environ["JWT_EXPIRE_IN"])
    ),
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}
JWT_SECRET = os.environ["JWT_SECRET"]


# PAYMENT SECRETS
SELLIX_KEY = os.environ['SELLIX_KEY']


# COMBO DOWNLOAD LIMIT
COMBO_DOWNLOAD_LIMIT = int(os.environ['COMBO_DOWNLOAD_LIMIT'])


# ENCRYPTION SECRETS
ENC_KEY = str.encode(os.environ["ENC_KEY"])


# PAGINATION
PAGE_SIZE = os.environ['PAGE_SIZE']


# CRON JOB FOR PROFILE
CRONJOBS = [
    ('0 0 * * *', 'cron.api.resetDownloads',
     '>> ' + str(BASE_DIR) + '/media/log/cron.log 2>&1')
]


# GOOGLE RECAPTCHA URL & KEYS
GOOGLE_VERIFY_RECAPTCHA_URL = os.environ["GOOGLE_VERIFY_RECAPTCHA_URL"]
RECAPTCHA_SECRET_KEY = os.environ["RECAPTCHA_SECRET_KEY"]


# MAILGUN CREDS
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']


# DATABASE CONFIGS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": os.environ["DB_ENGINE"],
#         "NAME": os.environ["DB_NAME"],
#         "USER": os.environ["DB_USER"],
#         "PASSWORD": os.environ["DB_PASSWORD"],
#         "HOST": os.environ["DB_HOST"],
#         'OPTIONS': {
#             "init_command": "SET GLOBAL max_connections = 100000",  # <-- The fix
#         }
#     }
# }


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR)+'/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_URL = os.environ["MEDIA_URL"]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
