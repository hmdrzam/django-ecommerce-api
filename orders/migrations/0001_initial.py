# Generated by Django 5.0.4 on 2024-06-03 12:08

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0002_address_profile"),
        ("products", "0006_category_image_count_product_ad_discount_percent_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "pending"),
                            ("S", "sending"),
                            ("D", "delivered"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("purchase_price", models.PositiveBigIntegerField()),
                ("shipping_price", models.PositiveBigIntegerField()),
                ("total_price", models.PositiveBigIntegerField(blank=True)),
                (
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.UUID("40978d78-e01a-4d91-a030-ffc166d50968"),
                        editable=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="accounts.address",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="orders.order",
                    ),
                ),
                (
                    "product_price",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_orders",
                        to="products.productprice",
                    ),
                ),
            ],
        ),
    ]
