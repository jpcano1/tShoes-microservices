""" Bill serializers """

# Django rest framework
from rest_framework import serializers

# Models
from .models import Bill

# Order serializers
from order.serializers import OrderModelSerializer

class BillModelSerializer(serializers.ModelSerializer):
    """ Bill Model Serializer """

    # The order related to the bill
    order = OrderModelSerializer(read_only=True)

    class Meta:
        """ Meta Class """
        model = Bill
        fields = '__all__'