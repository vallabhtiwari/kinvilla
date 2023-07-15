# Generated by Django 4.2.3 on 2023-07-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_resident_resident_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resident",
            name="id",
        ),
        migrations.AlterField(
            model_name="resident",
            name="resident_id",
            field=models.SlugField(
                editable=False, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
