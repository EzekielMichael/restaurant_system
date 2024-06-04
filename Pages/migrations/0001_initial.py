# Generated by Django 4.2.11 on 2024-06-01 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('ItemID', models.AutoField(primary_key=True, serialize=False)),
                ('ItemName', models.CharField(max_length=50)),
                ('ItemPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('OrderID', models.AutoField(primary_key=True, serialize=False)),
                ('OrderDate', models.DateField()),
                ('PaymentMethod', models.CharField(max_length=20)),
                ('TotalAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField()),
                ('ItemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pages.items')),
                ('OrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pages.orders')),
            ],
            options={
                'unique_together': {('OrderID', 'ItemID')},
            },
        ),
    ]