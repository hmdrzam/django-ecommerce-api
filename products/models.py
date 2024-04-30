from django.db import models


class Variation(models.Model):
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VariationOption(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='variation_options')
    name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    specifications = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    variation = models.ForeignKey(Variation, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.english_name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    variation_option = models.ForeignKey(VariationOption, on_delete=models.CASCADE, related_name='prices', null=True,
                                         blank=True)
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(blank=True, null=True)
    count = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.variation_option} - {self.product}'
