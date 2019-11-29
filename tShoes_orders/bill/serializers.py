""" Bill serializers """

# Django rest framework
from rest_framework import serializers

# Models
from .models import Bill

# Order serializers
from order.serializers import OrderModelSerializer

# Order model
from order.models import Order

# Item model
from item.models import Item

class BillModelSerializer(serializers.ModelSerializer):
    """ Bill Model Serializer """

    # The order related to the bill
    order = OrderModelSerializer(read_only=True)

    class Meta:
        """ Meta Class """
        model = Bill
        fields = '__all__'

class CreateBillSerializer(serializers.Serializer):
    """ Create Bill Serializer """

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    def validate_order(self, data):
        """
            Validates the order field
            :param data: is the order to be validated
            :exception: if the order is placed, generates exception
            :return: data validated
        """
        if data.status != 0:
            raise serializers.ValidationError('The order is placed')
        return data

    def create(self, data):
        """
            Bill model to be created
            :param data: the data that is going to be passed to the
            :return: the bill created after the entire process
        """
        # Total cost of the order
        total = 0
        order = data['order']
        # All the items in the order
        items = Item.objects.filter(order=order)
        for item in items:
            reference = item.reference
            # Hacer la petitición al backend de express
            if reference.stock < item.quantity:
                raise serializers.ValidationError(
                    "There are not enough references of this product: {}".format(str(reference))
                )
            reference.stock -= item.quantity
            total += item.quantity * reference.price
            reference.save()
        # Changes the status of the order
        order.status = 1
        order.save()
        bill = Bill.objects.create(order=order, total_price=total)
        self.send_order_confirmation(bill=bill)
        return bill

    @staticmethod
    def send_order_confirmation(bill):
        """
            Creates the notification order
            :return: None
        """


