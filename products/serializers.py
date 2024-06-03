from rest_framework import serializers
from products.models import Category, ProductPrice, Product, Variation, VariationOption


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return CategoryListSerializer(obj.get_children(), many=True).data

    class Meta:
        model = Category
        exclude = ('path', 'depth', 'numchild', 'active',)


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return CategoryListSerializer(obj.get_children(), many=True).data

    class Meta:
        model = Category
        fields = '__all__'


class VariationForProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'


class CategoryForProductListSerializier(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('path', 'depth', 'numchild',
                   'description', 'image_count', 'active')


class ProductListSerializer(serializers.ModelSerializer):
    variation = VariationForProductListSerializer(many=True)
    category = CategoryForProductListSerializier(many=True)

    class Meta:
        model = Product
        exclude = ('active', 'description', 'specifications', 'updated', 'created')


class VariationForProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'


class CategoryForProductRetriveSerializier(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('description', 'image_count', 'active')


class VariationOptionForProductRetrieveSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        exclude = ('variation',)


class ProductPriceForProductRetrieveSerializer(serializers.ModelSerializer):
    variation_option = VariationOptionForProductRetrieveSeriliazer(many=True)

    class Meta:
        model = ProductPrice
        exclude = ('product',)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    variation = VariationForProductListSerializer(many=True)
    category = CategoryForProductListSerializier(many=True)
    prices = ProductPriceForProductRetrieveSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
