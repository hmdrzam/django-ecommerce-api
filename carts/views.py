from rest_framework.exceptions import NotAcceptable

from carts.models import Cart
from carts.serializers import CartRetrieveSerializer, CartUpdateSerializer
from carts.viewsets import RetrieveListUpdateViewSet


class CartViewSet(RetrieveListUpdateViewSet):
    queryset = Cart.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'retrieve':
                return CartRetrieveSerializer
            case 'update':
                return CartUpdateSerializer
            case 'partial_update':
                return CartUpdateSerializer
            case _:
                raise NotAcceptable()
