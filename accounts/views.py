from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from accounts.models import Address
from accounts.serializers import AddressSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
