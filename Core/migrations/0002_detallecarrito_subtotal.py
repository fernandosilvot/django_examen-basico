# Generated by Django 5.0.4 on 2024-04-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="detallecarrito",
            name="subtotal",
            field=models.IntegerField(default=0),
        ),
    ]
