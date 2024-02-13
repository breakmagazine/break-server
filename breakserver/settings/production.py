from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com']

# 프로덕션 환경에 적합한 추가 보안 설정
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True