from .base import *

DEBUG = False

ALLOWED_HOSTS = ['http://3.36.128.9/', 'http://172.31.33.251/', 'http://127.0.0.1:8000/']

# 프로덕션 환경에 적합한 추가 보안 설정
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True