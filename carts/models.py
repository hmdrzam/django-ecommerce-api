from django.db import models
from products.models import ProductPrice
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")

    total = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s cart"

    def save(self, *args, **kwargs):
        if self.id:
            self.total = sum(x.product_price.final_price * x.quantity for x in self.cart_items.all())
            super(Cart, self).save()
        else:
            super(Cart, self).save()
            self.total = sum(x.product_price.final_price * x.quantity for x in self.cart_items.all())
            self.save(update_fields=('total',))


@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart}'s {self.product_price}"

    def save(self, *args, **kwargs):
        super(CartItem, self).save()
        self.cart.save()
