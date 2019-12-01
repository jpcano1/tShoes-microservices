""" Bill urls """
# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import *

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')

# Url patterns
urlpatterns = [
    path('', include(router.urls))
]