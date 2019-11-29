""" Item views """

# Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Item models
from .models import Item

# Order models
from order.models import Order

# Serializers
from .serializers import (ItemModelSerializer,
                          AddItemSerializer)

class ItemViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """ Item viewset """

    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """
            Inherited method to perform some actions needed before any request
            :param request: The request made by the user
            :param args: Some arguments carried on the request
            :param kwargs: Some Keyword arguments carried on the request
            :return: The supermethod dispath object with the actions
        """
        reference_id = kwargs['reference']
        self.reference = reference_id
        return super(ItemViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
            Creates the instance of the item
            :param request: the request object created from the request of the user
            :param args: Some arguments carried on the request
            :param kwargs: Some keyword arguments carried on the request
            :return: The serialized item created on the database
        """
        data = request.data.copy()
        data['reference'] = self.reference.id
        # Sends data to be validated
        serializer = AddItemSerializer(
            data=data,
            context={'request': request, 'stock': self.reference.stock}
        )
        # Validates data
        serializer.is_valid(raise_exception=True)
        # Saves object
        item = serializer.save()
        # Serializes object
        data = ItemModelSerializer(item).data
        return Response(data, status=status.HTTP_201_CREATED)

class CustomerItemViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """ Customer item viewset """

    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """ Defines permissions """
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

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
        self.customer = customer_id
        self.order = get_object_or_404(Order, customer=customer_id, id=order_id)
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