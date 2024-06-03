import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product, ProductPrice
from accounts.models import Address

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ("P", _("pending")),
        ("S", _("sending")),
        ("D", _("delivered")),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
    purchase_price = models.PositiveBigIntegerField()
    shipping_price = models.PositiveBigIntegerField()

    total_price = models.PositiveBigIntegerField(blank=True)
    uuid = models.UUIDField(default=uuid.uuid4(), db_index=True, editable=False, max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.buyer}'s {self.uuid} order"

    def save(self, *args, **kwargs):
        self.total_price = self.purchase_price + self.shipping_price
        super(Order, self).save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE, related_name="product_orders")
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order}'s {self.product_price}"
