from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, ProductViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

app_name = 'products'
urlpatterns = [

] + router.urls
