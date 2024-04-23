# Generated by Django 5.0.4 on 2024-04-22 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Core", "0002_detallecarrito_subtotal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registroenvio",
            name="detalle",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Core.detallecarrito",
            ),
        ),
    ]
