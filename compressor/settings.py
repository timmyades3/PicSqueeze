"""
Django settings for compressor project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('COMPRESSOR_SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!

if config('DEBUG') == 'False':
    DEBUG = False
else:
    DEBUG = True   

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','Timmyades3.pythonanywhere.com', ".vercel.app", ".now.sh"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # third party apps
    'social_django',
    'storages',
    'compressor1.apps.Compressor1Config',
    'users.apps.UsersConfig',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third party middlewares
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'users.middlewares.Onesessionperuser',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'compressor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # third party templates
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'compressor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#if DEBUG == True:
#    DATABASES = {
#        'default': {
#           'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': BASE_DIR / 'db.sqlite3',
#        }
#    }
#else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'HOST': config('PGHOST'),
        'PORT': config('PGPORT', 5432),
        'OPTIONS': {
        'sslmode': 'require',
        },
    }
    }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'users.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_PIPELINE = ('social_core.pipeline.social_auth.social_details',
                        'social_core.pipeline.social_auth.social_uid',
                        'social_core.pipeline.social_auth.social_user',
                        'social_core.pipeline.user.get_username',
                        'social_core.pipeline.social_auth.associate_by_email',
                        'social_core.pipeline.user.create_user',
                        'social_core.pipeline.social_auth.associate_user',
                        'social_core.pipeline.social_auth.load_extra_data',
                        'social_core.pipeline.user.user_details',
                        )

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = config('COMPRESSOR_SENDGRID_HOST_USER')
EMAIL_HOST_PASSWORD = config('COMPRESSOR_SENDGRID_SECRET_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'timileyinadesina1@gmail.com' 

AWS_ACCESS_KEY_ID = config('COMPRESSOR_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('COMPRESSOR_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('COMPRESSOR_AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = config('COMPRESSOR_AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

SOCIAL_AUTH_FACEBOOK_KEY = config('COMPRESSOR_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('COMPRESSOR_FACEBOOK_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('COMPRESSOR_GOOGLE_KEY') 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('COMPRESSOR_GOOGLE_SECRET_KEY')
SOCIAL_AUTH_TWITTER_KEY = config('COMPRESSOR_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config('COMPRESSOR_TWITTER_SECRET_KEY')
 
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'compress'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

