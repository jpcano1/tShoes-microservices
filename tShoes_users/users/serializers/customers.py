""" Customers Serializers """

# Django dependencies
from django.conf import settings

# Django rest framework
from rest_framework import serializers

# Users Serializers
from .users import UserSignUpSerializer

# Customer models
from ..models import Customer

# User Serializers
from .users import UserModelSerializer

class CustomerSignUpSerializer(UserSignUpSerializer, serializers.Serializer):
    """ Serializer of the sign up customer model,
        allows me to create new customers
    """

    # Basic data about localization: billind_address, city, country and zip code.
    billing_address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=255)

    def validate(self, data):
        super(CustomerSignUpSerializer, self).validate(data)
        return data

    def create(self, data):
        """
            Creates the user as a customer
            :param data: The validated data
            :return: The created customer
        """
        data.pop('password_confirmation')
        customer = Customer.objects.create_user(**data)
        self.confirmation(customer)
        return customer

class CustomerModelSerializer(serializers.ModelSerializer):
    """ Customer model serializer """

    class Meta:
        model = Customer
        fields = UserModelSerializer.Meta.fields.copy()
        fields.append('billing_address')
        fields.append('city')
        fields.append('country')
        fields.append('zip_code')
