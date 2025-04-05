from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_#z3u=!&qd+a@jh9lc-t1k!g^jt+p=$65=mv=h#5di5im2lqb+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

#     برای اضافه کردن اپشن ورود با گوگل👇
SITE_ID = 2
#     برای اضافه کردن اپشن ورود با گوگل 👆

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # project app:
    'tour',
    'tourism',
    'accounts',
    'news',
    'house',
    "scores",
    'cart',
    #     برای اضافه کردن اپشن ورود با گوگل👇
    "django.contrib.sites",
    # "users",
    "allauth",
    'allauth.account',
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    #     برای اضافه کردن اپشن ورود با گوگل 👆
]

#     برای اضافه کردن اپشن ورود با گوگل👇
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}
#     برای اضافه کردن اپشن ورود با گوگل 👆


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'djangoProject12.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'djangoProject12.wsgi.application'

# SQLite DATABASES👇

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Postcrest DATABASES👇


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # استفاده از پستگراس
#         'NAME': 'datap',                # نام پایگاه داده‌ای که ایجاد کردید
#         'USER': 'postgres',                      # نام کاربری
#         'PASSWORD': '13831383',                  # رمز عبور
#         'HOST': 'localhost',                          # می‌توانید IP سرور را نیز استفاده کنید
#         'PORT': '5432',                              # پورتی که PostgreSQL در آن کار می‌کند (معمولاً 5432 است)
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#     برای اضافه کردن اپشن ورود با گوگل👇
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
#     برای اضافه کردن اپشن ورود با گوگل 👆

#     برای اضافه کردن اپشن ارسال emile👇

# mail configurration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server host
EMAIL_PORT = 587  # SMTP server port (587 for TLS, 465 for SSL)
EMAIL_HOST_USER = 'aminhosseini822003@gmail.com'  # SMTP server username
EMAIL_HOST_PASSWORD = 'cdlv jard jzoh fhgo'  # SMTP server password
EMAIL_USE_TLS = True  # True for TLS, False for SSL
EMAIL_USE_SSL = False  # Set to True if using SSL

#    برای اضافه کردن اپشن ارسال emile👆
