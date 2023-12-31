# Generated by Django 4.2.3 on 2023-07-29 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_booking_applicant_alter_verification_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[("0", "In Process"), ("1", "Confirmed"), ("2", "Canceled")],
                default="0",
                max_length=1,
            ),
        ),
    ]
