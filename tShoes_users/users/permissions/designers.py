""" Designer permissions """

# Django rest framework
from rest_framework import permissions

# Models
from ..models.designers import Designer

class IsDesigner(permissions.BasePermission):
    """ Basic permission to verify the requesting user is designer """

    def has_permission(self, request, view):
        """
            Determines the requesting user is designer
            :param request: The request object
            :param view: The view where the requesting permission is comming from
            :return: A boolean
        """
        try:
            Designer.objects.get(id=request.user.id)
            return True
        except Designer.DoesNotExist:
            return False