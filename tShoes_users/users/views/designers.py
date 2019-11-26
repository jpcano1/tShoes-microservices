""" Designer viewset """

# Django rest framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

# Models
from ..models import Designer

# Serializers
from ..serializers import DesignerModelSerializer, DesignerSignUpSerializer

# Permissions
from ..permissions import (IsAccountOwner,
                           )

class DesignerViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin):
    """ The viewset of the designers """

    queryset = Designer.objects.all()
    serializer_class = DesignerModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """
            Cambiar a autenticacion real
            :return:
        """
        permissions = []
        if self.action in ['create']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAccountOwner]
            # permissions = [AllowAny]

        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """

            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        serializer = DesignerSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        designer = serializer.save()
        data = DesignerModelSerializer(designer).data
        return Response(data, status=status.HTTP_201_CREATED)
