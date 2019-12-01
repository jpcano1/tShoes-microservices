""" Item serializers """

# Django rest framework
from rest_framework import serializers

# Models
from .models import Item

# Order models
from  order.models import Order

class ItemModelSerializer(serializers.ModelSerializer):
    """ Item model serializer """

    reference = serializers.IntegerField()

    order = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        """
            Validate the data before creation
            :param data: The entire data that's going to be validated
            :return: The validated data
        """
        order = self.context['item'].order
        if order.status != 0:
            raise serializers.ValidationError("You cannot update this order")
        return data

    def validate_quantity(self, data):
        """ Validate some logic to the quantity field
            :param data: is the validation field
            :return: the data already validated
         """
        if data <= 0:
            raise serializers.ValidationError("Choose at least one reference")
        elif data > self.context['reference'].stock:
            raise serializers.ValidationError("There are not enough references")
        return data

    class Meta:
        """ Meta Class """
        model = Item
        exclude = ('created', 'modified')
        ordering = ('-created', '-modified')

class AddItemSerializer(serializers.Serializer):
    """ Add item serializer """

    # The quantity of items of some references that are going to be bought
    quantity = serializers.IntegerField()

    # The reference to be bought
    reference = serializers.IntegerField()

    def validate_quantity(self, data):
        """
            Validates quantity
            :return: the validated data
        """
        if data > self.context['stock']:
            raise serializers.ValidationError("There are not enough references to sell")
        elif data == 0:
            raise serializers.ValidationError("Choose at least one reference")
        return data

    def validate(self, data):
        """
            Validates the data that's going to be
            passed for creation of the item
            :param data the data that's going to be processed
            :return: the validated data
         """

        try:
            # Validates the customer already has an stateless order
            user = self.context['user']
            order = Order.objects.get(customer=user, status=0)
            data['order'] = order

            item = Item.objects.filter(reference=data['reference'], order=order)
            if item:
                raise serializers.ValidationError("You already choose this item in your order")
        except Order.DoesNotExist:
            pass
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Choose at least one reference")
        return data

    def create(self, data):
        """
            Creates the item with the validated data
            :param data: The validated data
            :return: the created item in the order
        """
        reference = data['reference']
        quantity = data['quantity']
        if data.get('order'):
            order = data['order']
        else:
            order = Order.objects.create(customer=self.context['user'])
        item = Item.objects.create(
            order=order,
            reference=reference,
            quantity=quantity
        )
        return item