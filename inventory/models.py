from django.db import models


class StockRoom(models.Model):
    name = models.CharField(max_length=200, help_text='maximum 200 characters')
    address = models.CharField(max_length=1024)
    stockroom_code = models.CharField(max_length=8)

    class Meta:
        ordering = ('stockroom_code',)

    def __str__(self):
        return f"{self.name}"


class StockItem(models.Model):
    product_price = models.ForeignKey('products.ProductPrice', on_delete=models.CASCADE, related_name='stock_items')
    sku = models.CharField(max_length=64, null=True, blank=True, unique=True)
    count = models.PositiveIntegerField(default=0)
    stockroom = models.ForeignKey(StockRoom, on_delete=models.PROTECT, related_name='stock_items')
    shortage_threshold = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('product_price', 'stockroom')
        ordering = ('sku',)

    def __str__(self):
        return f"{self.product_price} - {self.stockroom} stock item"
