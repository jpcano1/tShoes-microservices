""" Customers permissions """

# Django rest framework
from rest_framework.permissions import BasePermission

# Models
from ..models.customers import Customer

class IsCustomer(BasePermission):
    """ Basic permission to verify the requesting user is customer """

    def has_permission(self, request, view):
        """
            Determines the requesting user is a customer
            :param request: The request object
            :param view: The view where the request is comming from
            :return: A boolean
        """
        try:
            Customer.objects.get(id=request.user.id)
            return True
        except Customer.DoesNotExist:
            return False