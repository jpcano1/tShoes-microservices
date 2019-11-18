""" User models """

# Django dependencies
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utils
from utils.models import TShoesModel

class User(TShoesModel, AbstractUser):
    """
        User Model
        Extends from django's abstract base user
    """

    # The email for each user in the plaform
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    # Phone number regular expression to
    # check the number validation
    phone_regex = RegexValidator(
        regex=r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$',
        message='Phone number must be entered in the format: +9999999999. Up to 20 digits allowed.'
    )

    # Phone number of the user
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_regex]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # The identity for the user of the platform
    identification = models.CharField(
        'Identification document',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "A user with that id already exists"
        }
    )

    # Boolean that verifies the user is verified
    # in the platform
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user is verified')

    # Users profile picture
    profile_picture = models.ImageField(
        'Profile Image',
        upload_to='users/pictures',
        blank=True,
        null=True)

    def __str__(self):
        """ String function """
        return "{} - email: {} - identification: {}".format(self.username, self.email, self.identification)

    def get_short_name(self):
        """ Returns username """
        return self.username