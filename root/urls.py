from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

doc_patterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("products.urls", namespace="products")),
    path("api/inventory/", include("inventory.urls", namespace="inventory")),
    path("api/carts/", include("carts.urls", namespace="carts")),
    path("api/accounts/", include("accounts.urls", namespace="accounts")),
] + doc_patterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
