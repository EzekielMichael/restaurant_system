# Generated by Django 4.2.11 on 2024-06-04 12:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0008_alter_orders_ordertime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='OrderTime',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]