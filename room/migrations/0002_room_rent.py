# Generated by Django 4.2.3 on 2023-07-27 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="rent",
            field=models.DecimalField(decimal_places=2, default=8000.0, max_digits=7),
            preserve_default=False,
        ),
    ]
