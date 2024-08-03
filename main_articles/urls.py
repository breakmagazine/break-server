from django.urls import path
from .views import MainArticleView

urlpatterns = [
    path('', MainArticleView.as_view(), name='main-article-detail'),
]