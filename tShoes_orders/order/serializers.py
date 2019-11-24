""" Order serializer """

# Django rest framework
from rest_framework import serializers

# Order model
from order.models import Order

class ItemField(serializers.RelatedField):
    """ Item personalized serializer """

    def to_representation(self, value):
        """
            Method that allows me to make a representation of the field that I want to serialize
            :param value: The value that's going to be serialized
            :return: The serialized value.
        """
        data = {
            'id': value.id,
            'quantity': value.quantity,
            'reference': value.reference
        }
        return data

class OrderModelSerializer(serializers.ModelSerializer):
    """ Order model serializer """

    items = ItemField(many=True, read_only=True)

    class Meta:
        """ Meta class """
        model = Order
        fields = ['id',
                  'customer',
                  'optional_address',
                  'status',
                  'items']