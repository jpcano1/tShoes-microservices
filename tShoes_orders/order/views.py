""" Order views """

# Django rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models
from .models import Order

# Serializers
from .serializers import OrderModelSerializer

# Requests
import requests

class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    """ Order view set """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    lookup_field = 'id'

class CustomerOrderViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin):
    """ Customer order viewset """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        """
            Defines the permissions
            :return: an instance for each permission in the array
        """
        permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        customer_id = kwargs['customer']
        self.customer = customer_id
        return super(CustomerOrderViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            Retrieves the list of customers
            :param request: the request object
            :param args: the arguments of the request
            :param kwargs: the keyword arguments
            :return: The list of customers
        """
        customer = self.customer
        orders = Order.objects.filter(customer=customer)
        data = OrderModelSerializer(orders, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        customer = self.customer
        order = get_object_or_404(Order, customer=customer, id=kwargs['id'])
        if order.status == 0:
            order.delete()
        else:
            return Response("You can't delete this order", status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)



