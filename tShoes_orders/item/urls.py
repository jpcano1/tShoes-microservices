""" Item Urls """

# Django dependencies
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import *

router = DefaultRouter()
router.register(r'references/(?P<reference>[0-9]+)/item', ItemViewSet, basename='item')
router.register(r'customers/(?P<customer>[0-9]+)/orders/(?P<order>[0-9]+)/items', CustomerItemViewSet, basename='customer_item')

urlpatterns = [
    path('', include(router.urls))
]