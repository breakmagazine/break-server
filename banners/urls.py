from django.urls import path
from .views import MainBannerView, CentralBannerView

urlpatterns = [
    path('main/', MainBannerView.as_view(), name='main-banner'),
    path('mid/', CentralBannerView.as_view(), name='central-banner'),
]