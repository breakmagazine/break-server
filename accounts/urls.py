from django.urls import path, include
from accounts import views

urlpatterns = [
    path('kakao/login/', views.SocialLoginView.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.SocialLoginView.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('registration/', include('dj_rest_auth.registration.urls')),
]