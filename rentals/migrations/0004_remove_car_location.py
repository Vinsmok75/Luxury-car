# Generated by Django 4.2.7 on 2025-06-04 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_customer_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='location',
        ),
    ]
