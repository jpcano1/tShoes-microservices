""" Bill views """

# Django rest framework
from rest_framework import viewsets, mixins

# Bill Models
from .models import Bill

# Serializer
from .serializers import BillModelSerializer

class BillViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """ Bill Viewset """

    # The entire set of bills
    queryset = Bill.objects.all()
    # Serializer class
    serializer_class = BillModelSerializer
    # The field that's going to be looked for the detail methods
    lookup_field = 'id'
