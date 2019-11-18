# Django
from django.db import models

# Users Models
from users.models.users import User

class Designer(User, models.Model):
    """ Designer model """

    # Order address of the designer
    order_address = models.CharField(max_length=255, default=None)

    def __str__(self):
        """ String function """
        return f'By designer: {self.get_full_name()}'