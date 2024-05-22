from django.db import models
from treebeard.mp_tree import MP_Node
from products.managers import CategoryQuerySet


class Category(MP_Node):
    name = models.CharField(max_length=100, unique=True)
    english_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=130, unique=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.english_name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('media.Image', on_delete=models.PROTECT)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return f"{self.priority} - {self.category} image"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        for index, image in enumerate(self.category.images.all()):
            image.priority = index
            image.save()


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
    category = models.ManyToManyField(Category, related_name='products')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    variation = models.ManyToManyField(Variation, blank=True, related_name='products')

    def __str__(self):
        return self.english_name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    variation_option = models.ManyToManyField(VariationOption, blank=True)
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(blank=True, null=True)
    count = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{"-".join([i.name for i in self.variation_option.all()])} - {self.product}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('media.Image', on_delete=models.PROTECT)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return f"{self.priority} - {self.product} image"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        for index, image in enumerate(self.product.images.all()):
            image.priority = index
            image.save()
