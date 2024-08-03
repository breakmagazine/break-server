from django.urls import path
from .views import SymbolicView

urlpatterns = [
    path('', SymbolicView.as_view(), name='symbolic-detail'),
]