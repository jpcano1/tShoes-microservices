""" User views """

# Django rest framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
# Models
from ..models import User
# Serializers
from ..serializers import (UserModelSerializer,
                           UserSignUpSerializer,
                           AccountVerificationSerializer,
                           UserLoginSerializer)
from ..permissions import (IsAccountOwner, )

class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin):
    """
        user viewset
        handles Sign Up, login and account verification
    """

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = []
        if self.action in ['signup', 'login', 'verify', 'destroy']:
            permissions = [AllowAny]
        if self.action in ['update', 'partial_update', 'retrieve', 'list']:
            permissions = [IsAccountOwner]
        return [p() for p in permissions]

    def retrieve(self, request, *args, **kwargs):
        """
            Retrieve the user detail
            :param request: The request object
            :param args: Arguments
            :param kwargs: Keyword Arguments
            :return: the response given the request after validation
        """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = UserModelSerializer(response.data).data
        response.data = data
        return response

    @action(detail=False, methods=['post', 'get'])
    def verify(self, request):
        """
             Verifies an profile through token validation
            :param request: The request object
            :return: the response given the request after validation
        """
        data = {
            "token": request.query_params.get('token')
        }
        serializer = AccountVerificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "Message": "Congratulations, now go check the page!!!"
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
            Creates an user in the database with
            is_verified value = False
            :param request: The request object
            :return:
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
            User login
            :param request: The request objectS
            :return: The response with the data
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)