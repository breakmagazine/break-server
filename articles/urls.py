from django.urls import path
from .views import ArticleCreateView, ArticleDetailView, ArticleListByCategoryView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path("", ArticleCreateView.as_view(), name="article-create"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("all/", ArticleListByCategoryView.as_view(), name="article-list-by-category"),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete')
]
