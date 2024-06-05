from rest_framework import mixins, viewsets


class RetrieveListUpdateViewSet(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    pass
