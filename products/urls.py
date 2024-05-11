from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet

router = SimpleRouter()
router.register('category', CategoryViewSet, basename='category')

app_name = 'products'
urlpatterns = [

] + router.urls