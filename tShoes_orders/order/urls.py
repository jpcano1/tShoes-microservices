""" Order urls """

# Django dependencies
from django.urls import path, include

from rest_framework.routers import DefaultRouter

# views
from .views import *

router = DefaultRouter()
router.register(r'customers/(?P<customer>[0-9]+)/orders', CustomerOrderViewSet, basename='customer_order')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls))
]