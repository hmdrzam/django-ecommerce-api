from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CartViewSet

router = SimpleRouter()
router.register('carts', CartViewSet, basename='carts')

app_name = 'carts'
urlpatterns = [

] + router.urls
