from django.urls import path
from .views import CategoryImageView

urlpatterns = [
    path('category_images/<str:category>/', CategoryImageView.as_view(), name='category-image-detail'),
]