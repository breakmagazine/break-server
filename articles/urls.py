from django.urls import path
from .views import ArticleCreateView, ArticleDetailView, ArticleListByCategoryView

urlpatterns = [
    path("", ArticleCreateView.as_view(), name='article-create'),
    path("<int:pk>", ArticleDetailView.as_view(), name='article-detail'),
    path("all", ArticleListByCategoryView.as_view(), name='article-list-by-category'),
]