from django.contrib import admin
from .models import Variation, VariationOption, Product, ProductPrice

admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(Product)
admin.site.register(ProductPrice)
