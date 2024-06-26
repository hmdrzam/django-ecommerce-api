# Generated by Django 5.0.4 on 2024-06-03 12:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="uuid",
            field=models.UUIDField(
                db_index=True,
                default=uuid.UUID("c0357c2d-586a-4ac0-94db-cd8b02297752"),
                editable=False,
            ),
        ),
    ]
