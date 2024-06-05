from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import AddressViewSet

router = SimpleRouter()
router.register('addresses', AddressViewSet, basename='addresses')

app_name = 'accounts'
urlpatterns = [

] + router.urls
