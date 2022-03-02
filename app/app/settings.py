from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dr%hqgpi(=dtj41u$c2qrzu9mcdnd9tkz@#*d%vm+zt9t(r&d+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['football-players-stats-api.herokuapp.com','127.0.0.1']

# Application definition

CORS_ALLOW_ALL_ORIGINS = True                         
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS    = [ 'https://football-players-stats-api.herokuapp.com',] 
CORS_ALLOWED_ORIGIN_REGEXES = [ 'https://football-players-stats-api.herokuapp.com',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'database',
    'web_scraping',
    'api',
    'accounts',

    'rest_framework',
    'rest_framework.authtoken',
    'django_q',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql', 
        'NAME'     : 'd2fcrdpv7dt8bs',
        'HOST'     : 'ec2-3-232-13-123.compute-1.amazonaws.com',
        'USER'     : 'xnfinaovuftosm',
        'PASSWORD' : 'd1256340251269a44021edb54c6731ad76ae034263433951ed34218e06ade3db',
        'PORT'     : 5432,
        }        
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
import os

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


AUTH_USER_MODEL = 'accounts.User'

Q_CLUSTER = {
    'name': 'football_players_stats',
    'workers': 1,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': 'ec2-3-212-6-179.compute-1.amazonaws.com',
        'password': 'p6ae4713d213913af5e365dbf58752a7bc87f597a216952ee0cb0aaa6865825f5',
        'port': 21909,
        'db': 0, }
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import django_heroku


django_heroku.settings(locals())

