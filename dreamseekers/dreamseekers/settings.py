import os
import json
from pathlib import Path
import sys

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_BASE_FILE = "dreamseekers/secrets.json"

secrets = json.load(open(SECRET_BASE_FILE))
for key, value in secrets.items():
    setattr(sys.modules[__name__],key,value)

SECRET_KEY = secrets.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'dreamsdb'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '1234'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# 현재 폴더 기본 위치
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 로그인 모델 변경
AUTH_USER_MODEL = 'user.Users'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['localhost', '127.0.0.1',]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'user',
    'board',
    'comment',
    'lecture',
    'blog',
    'notice',
    'intro',
    'archive',
    
    'corsheaders',

    # DRF
    'rest_framework',
    'rest_framework.authtoken',

    # allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # allauth - naver
    'allauth.socialaccount.providers.naver',

     # dj_rest_auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    # token
    'rest_framework_simplejwt',

    # pycryptodome
    'Crypto',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ORIGIN_WHITELSIT = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

ROOT_URLCONF = 'dreamseekers.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'intro.context_processors.footer',
            ],
        },
    },
]

WSGI_APPLICATION = 'dreamseekers.wsgi.application'

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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
ROOT_DIR = os.path.dirname(BASE_DIR)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATIC_DIR = os.path.join(BASE_DIR,'dreamseekers', 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#이미지 저장
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#로그인/아웃 성공시 이동하는 URL
LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

# rest framework 에 대한 설정
REST_FRAMEWORK = {
    # 기본 인증에 대한 설정
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # dj_rest_auth 의 인증 절차 중 JWTCookieAuthentication을 사용
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    # 허가에 대한 설정
    'DEFAULT_PERMISSION_CLASSES': (
    	# 인증이 완료된 사용자에 한해서 접근 허가
        'rest_framework.permissions.IsAuthenticated',
    )
}

# cookie key 와 refresh cookie key 의 이름을 설정
JWT_AUTH_COOKIE = 'sociallogin-auth'
JWT_AUTH_REFRESH_COOKIE = 'sociallogin-refresh-token'

# JWT 사용을 위한 설정
REST_USE_JWT = True

# simplejwt 에 대한 설정
SIMPLE_JWT = {
    # access token 의 유효기간
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    # refresh token 의 유효기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    # 토큰에 들어갈 알고리즘
    'ALGORITHM': 'HS256',
    # 토큰을 만드는데 사용할 secret key
    'SIGNING_KEY': SECRET_KEY,
}

# 이미지 최대 용량 (MB)
MAX_IMAGE_SIZE = 20
# 사용자별 최대 이미지 개수
MAX_IMAGE_COUNT = 5

# 이메일 설정
EMAIL = secrets.get('EMAIL_NAME') + '@naver.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = secrets.get('EMAIL_NAME')
EMAIL_HOST_PASSWORD = secrets.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER