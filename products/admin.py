from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Variation, VariationOption, Product, ProductPrice, Category

admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(Product)
admin.site.register(ProductPrice)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Category, CategoryAdmin)
