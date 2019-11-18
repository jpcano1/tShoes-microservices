""" Customer model """

# Django dependencies
from django.db import models

# User models
from .users import User

class Customer(User, models.Model):
    """ Class that represents the customer
        Model from tShoes.
    """

    # Billing address of the user customer
    billing_address = models.CharField(max_length=255, default=None, null=True)

    # City where the customer lives
    city = models.CharField(max_length=255, default=None, null=True)

    # Country where the customer lives
    country = models.CharField(max_length=255, default=None, null=True)

    # Zip code of the house of the customer
    zip_code = models.PositiveIntegerField(default=0)

    def __str__(self):
        """ toString function """
        return "Customer with name: {} and address: {}".format(self.first_name + " " + self.last_name,
                                                               str(self.billing_address))