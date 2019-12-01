""" Order views """

# Django rest framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

# Models
from .models import Order

# Serializers
from .serializers import OrderModelSerializer

# Requests
import requests

import environ

# Bill serializer
from bill.serializers import CreateBillSerializer, BillModelSerializer

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
    env = environ.Env()
    users_url = env('CUSTOMERS', default='http://0.0.0.0:8000')

    def dispatch(self, request, *args, **kwargs):
        customer_id = kwargs['customer']
        req = requests.get(self.users_url + f'/customers/{customer_id}/', headers=request.headers)
        if req.status_code == 200:
            self.customer = {
                "status": req.status_code,
                "customer": req.json().get('id')
            }
        else:
            self.customer = {
                "status": req.status_code,
                "customer": req.json()
            }
        return super(CustomerOrderViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            Retrieves the list of customers
            :param request: the request object
            :param args: the arguments of the request
            :param kwargs: the keyword arguments
            :return: The list of customers
        """
        if self.customer['status'] == 200:
            customer = self.customer.get("customer")
            orders = Order.objects.filter(customer=customer)
            data = OrderModelSerializer(orders, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(self.customer["customer"], status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if self.customer['status'] == 200:
            customer = self.customer.get("customer")
            order = get_object_or_404(Order, customer=customer, id=kwargs['id'])
            if order.status == 0:
                order.delete()
            else:
                return Response("You can't delete this order", status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(self.customer["customer"], status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def place(self, request, *args, **kwargs):
        """
            Places an order
            :param request: the request object
            :param args: the arguments of the request
            :param kwargs: the keyword arguments
            :return: The bill created
        """
        if self.customer['status'] == 200:
            order = get_object_or_404(Order, id=kwargs['id'], customer=self.customer["customer"])
            serializer = CreateBillSerializer(data={
                'order': order.id
            })
            serializer.is_valid(raise_exception=True)
            bill = serializer.save()
            data = BillModelSerializer(bill).data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(self.customer["customer"], status=status.HTTP_400_BAD_REQUEST)