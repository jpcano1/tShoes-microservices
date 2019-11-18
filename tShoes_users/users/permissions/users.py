""" Users Permissions """

# Django rest framework
from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    """ Allow access only to accouts owned by the requesting user """

    def has_object_permission(self, request, view, obj):
        """
            Validates the requesting user is the account owner
            :param request: The request param
            :param view: the view which is requesting the permission
            :param obj: The object being requested
            :return: A boolean that determines whether
            the requesting user has access or not
        """
        return request.user.id == obj.id

class IsVerified(permissions.BasePermission):
    """ Allows to validate the requesting user is verified """

    def has_permission(self, request, view):
        """
            Validates the requesting user is verified
            :param request: The request object
            :param view: the view which is requesting the permission
            :return: A boolean that determines whether
            the requesting user has access or not
        """
        return request.user.is_verified