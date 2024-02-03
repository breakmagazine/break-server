from django.urls import path, include
from accounts import views

urlpatterns = [
    path("kakao/login/", views.kakao_login, name="kakao_login"),
    path("kakao/callback/", views.kakao_callback, name="kakao_callback"),
    path(
        "kakao/login/finish/", views.KakaoLoginView.as_view(), name="kakao_login_todjango"
    ),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("join/", views.UpdateUserInfoView.as_view(), name="update_user_info"),
]
