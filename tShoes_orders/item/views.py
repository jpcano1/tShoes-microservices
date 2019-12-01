""" Item views """

# Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

# Item models
from .models import Item

# Order models
from order.models import Order

# Serializers
from .serializers import (ItemModelSerializer,
                          AddItemSerializer)

import environ

import requests
import json

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """ Item viewset """

    env = environ.Env()
    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'
    users_url = env('CUSTOMERS', default='http://0.0.0.0:8000')
    references_url = env('REFERENCES', default='http://0.0.0.0:3001')

    def dispatch(self, request, *args, **kwargs):
        """
            Inherited method to perform some actions needed before any request
            :param request: The request made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: The supermethod dispath object with the actions
        """
        reference_id = kwargs['reference']
        req = requests.get(self.references_url + f'/references/{reference_id}')
        if req.status_code == 200:
            self.reference = req.json()
        else:
            self.reference = None
        return super(ItemViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
            Creates the instance of the item
            :param request: the request object created from the request of the user
            :param args: Some arguments carried on the request
            :param kwargs: Some keyword arguments carried on the request
            :return: The serialized item created on the database
        """
        req = requests.get(self.users_url + '/customers/token/', headers=request.headers)
        if req.status_code == 200 and self.reference:
            data = request.data.copy()
            data['reference'] = self.reference.get('id')
            # Sends data to be validated
            serializer = AddItemSerializer(
                data=data,
                context={
                    'user': req.json().get('id'),
                    'stock': self.reference.get('stock')
                }
            )
            # Validates data
            serializer.is_valid(raise_exception=True)
            # Saves object
            item = serializer.save()
            # Serializes object
            data = ItemModelSerializer(item).data

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            if req.status_code != 200:
                return Response(req.json(), status=status.HTTP_401_UNAUTHORIZED)
            elif not self.reference:
                return Response(status=status.HTTP_404_NOT_FOUND)

class CustomerItemViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """ Customer item viewset """

    env = environ.Env()
    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'
    users_url = env('CUSTOMERS', default='http://0.0.0.0:8000')

    def dispatch(self, request, *args, **kwargs):
        """
              Inherited method to perform some actions needed before any request
              :param request: The request made by the user
              :param args: Some arguments carried on the request
              :param kwargs: Some Keyword arguments carried on the request
              :return: The supermethod dispatch object with the actions
        """
        customer_id = kwargs['customer']
        order_id = kwargs['order']
        req = requests.get(self.users_url + f'/customers/{customer_id}/', headers=request.headers)
        self.customer = {
            "status": req.status_code,
            "customer": req.json().get('id')
        }
        self.order = get_object_or_404(Order, customer=self.customer.get('customer'), id=order_id)
        return super(CustomerItemViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            Lists items
            :param request: The request made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: The list of items
        """
        items = Item.objects.filter(order=self.order)
        data = ItemModelSerializer(items, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
            updates an item
            :param request: The request made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: the response object
        """
        item = get_object_or_404(Item, id=kwargs['id'])
        partial = request.method == 'PATCH'
        serializer = ItemModelSerializer(item, data=request.data, context={
            'reference': item.reference,
            'item': item
        }, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ItemModelSerializer(item).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
            Deletes an item from the order
            :param request: The request made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: The response object
        """
        item = get_object_or_404(Item, id=kwargs['id'])
        order = item.order
        item.delete()
        if order.items.count() == 0:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)