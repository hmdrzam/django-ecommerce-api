from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .forms import ProductPriceAdminForm
from .models import Variation, VariationOption, Product, ProductPrice, Category

admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(Product)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Category, CategoryAdmin)


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    form = ProductPriceAdminForm
