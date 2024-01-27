from django.contrib import admin
from django.urls import include, path, re_path
from .views import kakao_login_page
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from accounts.urls import urlpatterns as accounts_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Break-Magazine API",
        default_version='v1',
        description="API documentation for Break-Magazine Webzine project",
    ),
    public=True,
    patterns=accounts_urlpatterns,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('', kakao_login_page, name='home'),
   path('admin/', admin.site.urls),
   # path('accounts/', include('dj_rest_auth.urls')),
   # path('accounts/', include('dj_rest_auth.registration.urls')),
   path('allauth/', include('allauth.urls')),
   path('accounts/', include('accounts.urls')),
   path('accounts/social/', include('allauth.socialaccount.urls'), ),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]