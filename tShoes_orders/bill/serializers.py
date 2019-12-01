""" Bill serializers """

# Django dependencies
from django.template.loader import render_to_string

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

import requests

import environ

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
    env = environ.Env()
    users_url = env('CUSTOMERS', default='http://0.0.0.0:8000')
    references_url = env('REFERENCES', default='http://0.0.0.0:3001')

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
            reference_id = item.reference
            req = requests.get(self.references_url + f'/references/{reference_id}')
            reference = req.json()
            # Hacer la petitición al backend de express
            if reference["stock"] < item.quantity:
                raise serializers.ValidationError(
                    "There are not enough references of this product: {}".format(reference['referenceName'])
                )
            new_stock = reference["stock"] - item.quantity
            body = {
                "stock": new_stock
            }
            requests.put(self.references_url + f'/references/{reference_id}', data=body)
            total += item.quantity * reference["price"]
        # Changes the status of the order
        order.status = 1
        order.save()
        bill = Bill.objects.create(order=order, total_price=total)
        return bill

    @staticmethod
    def send_order_confirmation(self, bill):
        """
            Creates the notification order
            :return: None
        """
        subject = "Order created"
        from_email = "tShoes Store <noreply@tShoes.com>"
        message = f"Your order {bill.order.id} has been placed"
        message += "id: {} \n".format(bill.id)
        message += "items: \n"
        for item in bill.order.items.all():
            req = requests.get(self.references_url + f'/references/{item.reference}')
            reference = req.json()
            message += f"id: {reference.get('id')} \n"
            message += f"name: {reference.get('referenceName')} \n"
        message += f"total price {bill.total_price} \n"
        message += "Thanks for buying with tShoes"
        content = render_to_string(
            'emails/bill/customer_bill.html',
            {
                'message': message
            })