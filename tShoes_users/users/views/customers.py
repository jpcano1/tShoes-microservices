""" Customer views """

# Django rest framework
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

# Models
from ..models import Customer

# Serializer
from ..serializers import (CustomerModelSerializer,
                           CustomerSignUpSerializer)

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..permissions import IsAccountOwner

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
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permissions = [IsAccountOwner,
                           IsAuthenticated]
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """

            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        serializer = CustomerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        data = CustomerModelSerializer(customer).data
        return Response(data, status=status.HTTP_201_CREATED)

