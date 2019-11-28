""" Bill model """

# Django dependencies
from django.db import models

# Utils models
from utils.models import TShoesModel

class Bill(TShoesModel, models.Model):
    """ Class that represents the bill of the order """

    # The order that owns the bill
    order = models.OneToOneField('order.Order', on_delete=models.CASCADE, related_name='bill')

    # Total price of the
    total_price = models.FloatField(default=0)

    def __str__(self):
        """ toString function """
        return f"id of the bill: {self.id} and the total price: {self.total_price}"
