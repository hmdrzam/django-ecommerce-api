from rest_framework import serializers
from products.models import Category


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
