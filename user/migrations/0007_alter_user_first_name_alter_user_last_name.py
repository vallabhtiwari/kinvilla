# Generated by Django 4.2.3 on 2023-08-01 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_user_is_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=50),
        ),
    ]
