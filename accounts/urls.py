from django.urls import path, include
from accounts import views
def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if not path.startswith("/accounts/registration/"):
            filtered.append((path, path_regex, method, callback))
    return filtered

urlpatterns = [
    path('kakao/login/', views.SocialLoginView.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.SocialLoginView.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('join/', views.UpdateUserInfoView.as_view(), name='update_user_info'),
    path('registration/', include('dj_rest_auth.registration.urls'))
]