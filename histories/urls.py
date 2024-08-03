from django.urls import path
from .views import HistoryListCreateView, HistoryDetailView

urlpatterns = [
    path('', HistoryListCreateView.as_view(), name='history-list-create'),
    path('<int:publication_number>/', HistoryDetailView.as_view(), name='history-detail'),
]