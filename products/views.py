from rest_framework.exceptions import NotAcceptable
from rest_framework.viewsets import ReadOnlyModelViewSet
from products.models import Category
from products.serializers import CategoryListSerializer, CategoryRetrieveSerializer


class CategoryViewSet(ReadOnlyModelViewSet):

    def get_queryset(self):
        match self.action:
            case 'list':
                return Category.objects.depth().active()
            case 'retrieve':
                return Category.objects.active()
            case _:
                return NotAcceptable

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CategoryListSerializer
            case 'retrieve':
                return CategoryRetrieveSerializer
            case _:
                return NotAcceptable
