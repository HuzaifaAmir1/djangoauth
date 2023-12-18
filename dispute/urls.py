# in dispute/urls.py
from django.urls import path
from .views import DisputeListCreateView, DisputeUpdateResolvedView

urlpatterns = [
    path('disputes/', DisputeListCreateView.as_view(), name='dispute-list-create'),
    path('disputes/resolve/<int:pk>/', DisputeUpdateResolvedView.as_view(), name='dispute-update-resolved'),
]
