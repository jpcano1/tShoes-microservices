""" Designer Serializer """
# Django dependencies
from django.conf import settings

# Django Rest framework
from rest_framework import serializers

# Serializer
from .users import UserSignUpSerializer, UserModelSerializer

# Models
from users.models import Designer

# Auth0 dependencies
from auth0.v2 import authentication

class DesignerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up designer model, allows me to create new designers """

    database = authentication.Database(domain=settings.SOCIAL_AUTH_AUTH0_DOMAIN)

    # Order address of the designer, where the reference is picked up
    order_address = serializers.CharField(max_length=255)

    def validate(self, data):
        super(DesignerSignUpSerializer, self).validate(data)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        self.database.signup(client_id=settings.SOCIAL_AUTH_AUTH0_KEY,
                             email=data['email'],
                             password=data['password'],
                             connection=settings.AUTH0_DATABASE_CONNECTION)
        designer = Designer.objects.create_user(**data)
        self.send_confirmation_email(designer)
        return designer

class DesignerModelSerializer(serializers.ModelSerializer):
    """ The model serializer of designers """

    class Meta:
        """ Meta class """
        model = Designer
        fields = UserModelSerializer.Meta.fields.copy()
