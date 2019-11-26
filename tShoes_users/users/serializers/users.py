""" User Serializer """

# Django models
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, password_validation
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Django Rest Framework models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from users.models import User

# Utilities
from jose import jwt
from jose import *
from django.utils import timezone
from datetime import timedelta

# Auth0 Dependencies
from auth0.v2 import authentication

class AccountVerificationSerializer(serializers.Serializer):
    """
        Account verification Serializer that allows to know which user has a
        verificated account and which doesn't
    """

    token = serializers.CharField()

    def validate(self, data):
        """ Validate method for the token """
        try:
            payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise serializers.ValidationError("The token has expired.")
        except JWTError:
            raise serializers.ValidationError("Error validating token. Ensure is the right token.")

        self.context['payload'] = payload
        return data

    def save(self, **kwargs):
        """ Update the user's verification status """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

class UserLoginSerializer(serializers.Serializer):
    """ User login Serializer
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)

    def validate(self, data):
        """ Check credentials. """
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid Credentials')

        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet")

        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate or retrieve new Token """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):
    """ Class that allows us to create users and to send
        verification token to the user through the email.
    """
    
     # Username of the user
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Email field
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Identification field
    identification = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Phone regular expression
    phone_regex = RegexValidator(
        regex=r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$',
        message='Invalid phone number format'
    )

    # phone number field
    phone_number = serializers.CharField(validators=[phone_regex], required=True)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # First_name and last_name of the username
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Image of the user
    profile_picture = serializers.ImageField(required=False, default=None)

    def validate(self, data):
        passwd = data['password']
        passwd_confirmation = data['password_confirmation']

        if passwd_confirmation != passwd:
            raise serializers.ValidationError("Passwords don't match")

        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        """
            Creates user
            :param data: the validated data
            :return: the created user
        """
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """ Send account verification link to given user """
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to start using Comparte Ride'
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user
            })
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach(content, 'text/html')
        msg.send()
        print("Sending email")

    def gen_verification_token(self, user):
        """
            create JWT token that the user can use to verify its account
            :param user: The new user to be verified
            :return: The token of the new user
        """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

class UserModelSerializer(serializers.ModelSerializer):
    """ This class respresents the user model serializer """

    class Meta:
        """ Meta class """
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'identification',]