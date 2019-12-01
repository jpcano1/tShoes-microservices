""" Item Urls """

# Django dependencies
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import *

router = DefaultRouter()
router.register(r'references/(?P<reference>[0-9]+)/item', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls))
]