from rest_framework import routers
from .views import JobProposalViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register(r'job-proposals', JobProposalViewSet)

urlpatterns = [
    # ...
    path('', include(router.urls)),
    # ...
]
