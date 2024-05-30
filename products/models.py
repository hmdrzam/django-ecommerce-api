from django.db import models
from treebeard.mp_tree import MP_Node
from products.managers import CategoryQuerySet
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(MP_Node):
    name = models.CharField(max_length=100, unique=True)
    english_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=130, unique=True)

    image_count = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.english_name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.image_count = len(self.images.all())
        super(Category, self).save(update_fields=('image_count',))


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

    def save(self, *args, **kwargs):
        category = CategoryImage.objects.get(id=self.id).category
        super(CategoryImage, self).save(*args, **kwargs)
        self.category.save()
        category.save()


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
    variation = models.ManyToManyField(Variation, blank=True, related_name='products')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ad_price = models.PositiveBigIntegerField(null=True, blank=True)
    image_count = models.PositiveSmallIntegerField(null=True, blank=True)
    counts = models.PositiveSmallIntegerField(null=True, blank=True)
    sell_count = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    ad_discount_percent = models.PositiveSmallIntegerField(validators=(MinValueValidator(0), MaxValueValidator(100)),
                                                           null=True, blank=True)

    def __str__(self):
        return self.english_name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.ad_price = min((x.final_price for x in self.prices.all()), default=None)
        self.counts = sum(x.count for x in self.prices.all())
        self.sell_count = sum(x.sell_count for x in self.prices.all())
        self.image_count = len(self.images.all())
        self.slug = slugify(self.english_name, allow_unicode=True)
        self.ad_discount_percent = max((x.discount_percent for x in self.prices.all()), default=None)

        if self.counts:
            self.available = True
        else:
            self.available = False
        super(Product, self).save(
            update_fields=(
                'ad_price', 'counts', 'sell_count', 'image_count', 'slug', 'ad_discount_percent', 'available'))


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    variation_option = models.ManyToManyField(VariationOption, blank=True)
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(blank=True, null=True)
    upc = models.CharField(max_length=24, unique=True, null=True, blank=True)

    count = models.PositiveSmallIntegerField(default=0)
    sell_count = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    discount = models.BooleanField(default=False)
    discount_percent = models.PositiveSmallIntegerField(validators=(MinValueValidator(0), MaxValueValidator(100)),
                                                        null=True, blank=True)
    final_price = models.PositiveBigIntegerField(null=True, blank=True)
    customer_profit = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        vo = self.variation_option.all()
        return f'{"-".join([i.name for i in vo])} {"-" if len(vo) else ""} {self.product}'

    def save(self, *args, **kwargs):
        if self.id:
            pre_product = ProductPrice.objects.get(id=self.id).product
            if self.discount_price:
                dp = 100 - (self.discount_price * 100) / self.price
                self.discount_percent = math.ceil(dp)
                self.final_price = self.discount_price
                self.customer_profit = self.price - self.discount_price
            else:
                self.discount_percent = 0
                self.final_price = self.price
                self.customer_profit = 0

            if self.discount_percent == 0:
                self.discount = False
            else:
                self.discount = True

            self.count = sum((x.count for x in self.stock_items.all()))

            if self.count:
                self.available = True
            else:
                self.available = False

            super(ProductPrice, self).save(*args, **kwargs)
            self.product.save()
            if pre_product != self.product:
                pre_product.save()
        else:
            super(ProductPrice, self).save(*args, **kwargs)
            if self.discount_price:
                dp = 100 - (self.discount_price * 100) / self.price
                self.discount_percent = math.ceil(dp)
                self.final_price = self.discount_price
                self.customer_profit = self.price - self.discount_price
            else:
                self.discount_percent = 0
                self.final_price = self.price
                self.customer_profit = 0

            if self.discount_percent == 0:
                self.discount = False
            else:
                self.discount = True

            self.count = sum((x.count for x in self.stock_items.all()))

            if self.count:
                self.available = True
            else:
                self.available = False

            super(ProductPrice, self).save(
                update_fields=(
                    'discount_percent', 'final_price', 'customer_profit', 'discount', 'count', 'available',
                    'sell_count'))
            self.product.save()


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

    def save(self, *args, **kwargs):
        if self.id:
            pre_product = ProductImage.objects.get(id=self.id).product
            super(ProductImage, self).save(*args, **kwargs)
            self.product.save()

            if pre_product != self.product:
                pre_product.save()
        else:
            super(ProductImage, self).save(*args, **kwargs)
            self.product.save()
