from django.contrib import admin

from .models import StockRoom, StockItem

admin.site.register(StockRoom)
admin.site.register(StockItem)
