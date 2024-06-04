from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Orders(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    OrderDate = models.DateField(null=False)
    OrderTime = models.TimeField(default=timezone.now, null=False)
    PaymentMethod = models.CharField(max_length=20, null=False)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2, null=False)

class Items(models.Model):
    ItemID = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=50, null=False)
    ItemPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ItemImage = models.FileField(upload_to='uploads/Items')

    def __str__(self):
        return self.ItemName

class OrderItems(models.Model):
    OrderID = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False)
    ItemID = models.ForeignKey(Items, on_delete=models.CASCADE, null=False)
    Quantity = models.IntegerField(null=False)
    Status = models.CharField(default='pending')

    class Meta:
        unique_together = ('OrderID', 'ItemID')



class Table1(models.Model):
    col1 = models.CharField(max_length=50, null=False)
    col2 = models.CharField(max_length=50, null=False)

class Table2(models.Model):
    col1 = models.CharField(max_length=50, null=False)
    col2 = models.ForeignKey(Table1, on_delete=models.CASCADE, null=False)