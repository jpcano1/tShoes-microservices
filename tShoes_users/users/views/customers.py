""" Customer views """

# Django rest framework
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# Models
from ..models import Customer

# Serializer
from ..serializers import (CustomerModelSerializer,
                           CustomerSignUpSerializer)

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..permissions import IsAccountOwner, IsCustomer

class CustomerViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    """ Customer viewset """
    queryset = Customer.objects.all()
    serializer_class = CustomerModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = []
        if self.action in ['create']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update', 'retrieve', 'token']:
            permissions = [IsAccountOwner,
                           IsAuthenticated,
                           IsCustomer]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """
            Creates user as a customer
            :param request: the request object
            :param args: arguments of the request
            :param kwargs: keyword arguments of the request
            :return: the created
        """
        serializer = CustomerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        data = CustomerModelSerializer(customer).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def token(self, request, *args, **kwargs):
        """
            Retrieves a user by its token
            :param request: the request object
            :param args: the arguments of the request
            :param kwargs: the keyword arguments of the request
            :return: the user requested
        """
        serializer = CustomerModelSerializer(request.user).data
        return Response(serializer, status=status.HTTP_200_OK)