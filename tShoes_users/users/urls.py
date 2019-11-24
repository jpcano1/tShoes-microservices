""" User urls """

# Django dependencies
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views
from .views import designers as designer_views
from .views import customers as customer_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'designers', designer_views.DesignerViewSet)
router.register(r'customers', customer_views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]