from rest_framework import serializers
from carts.models import Cart, CartItem
from products.models import ProductPrice
from products.serializers import ProductPriceForCartRetrieveSerializer, ProductPriceForCartUpdateSerializer
from rest_framework.exceptions import APIException


class CartItemRetrieveSerializer(serializers.ModelSerializer):
    product_price = ProductPriceForCartRetrieveSerializer()

    class Meta:
        model = CartItem
        exclude = ('cart',)


class CartRetrieveSerializer(serializers.ModelSerializer):
    cart_items = CartItemRetrieveSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('total', 'user',)


# Cart updating serializers
class CartItemUpdateSerializer(serializers.ModelSerializer):
    product_price = ProductPriceForCartUpdateSerializer()

    class Meta:
        model = CartItem
        exclude = ('cart',)


class CartUpdateSerializer(serializers.ModelSerializer):
    cart_items = CartItemUpdateSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('total', 'user',)

    def update(self, instance, validated_data):
        cart_items = validated_data.pop('cart_items', [])
        new_product_prices = {}
        existing_product_prices = {}
        for cart_item in cart_items:
            new_product_prices[cart_item.get('product_price').get('id')] = cart_item.get('quantity')

        e_product_prices = instance.cart_items.all()

        for product_price in e_product_prices:
            existing_product_prices[product_price.product_price.id] = product_price.quantity

        for obj in new_product_prices.keys():
            if new_product_prices.get(obj) > ProductPrice.objects.get(id=obj).count:
                raise APIException('the quantity is more than product count')

        if new_product_prices != existing_product_prices:
            for obj in new_product_prices.keys():
                if existing_product_prices.get(obj) == None:
                    CartItem.objects.create(cart=instance, product_price_id=obj,
                                            quantity=new_product_prices[obj]).save()
                else:
                    modified_cart_item = CartItem.objects.get(cart=instance, product_price_id=obj)
                    modified_cart_item.quantity = new_product_prices.get(obj)
                    modified_cart_item.save()

            for obj in existing_product_prices.keys():
                if new_product_prices.get(obj) == None:
                    CartItem.objects.get(cart=instance, product_price_id=obj).delete()

        instance.save()
        return instance
