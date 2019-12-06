""" Bill serializers """

# Django dependencies
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

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

from tShoes_orders.connection import Authtoken

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
    token = Authtoken()

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
        self.send_order_confirmation(bill)
        return bill

    def send_order_confirmation(self, bill):
        """
            Creates the notification order
            :return: None
        """
        # orderId, billId, referenceId, referenceName, referencePrice, totalPrice
        plain = get_template('emails/bill/customer_bill.txt')
        html = get_template('emails/bill/customer_bill.html')
        to_email = self.token.fetch_user_by_id(bill.order.customer)
        subject = "Order placed"
        from_email = "tShoes <noreply@tShoes.com>"
        references = []
        for item in bill.order.items.all():
            req = requests.get(self.references_url + f'/references/{item.reference}')
            data = req.json()
            reference = {
                'id': data.get('id'),
                'name': data.get('referenceName'),
                'price': data.get('price')
            }
            references.append(reference)
        data = {
            "order_id": bill.order.id,
            "bill_id": bill.id,
            "references": references,
            "total_price": bill.total_price
        }
        text_content, html_content = plain.render(data), html.render(data)
        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Sending email")