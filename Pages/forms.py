from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import models, Items, OrderItems, Orders

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['PaymentMethod']

    def save(self, customer, items):
        order = Orders.objects.create(
            CustomerID=customer,
            OrderDate=timezone.now(),
            PaymentMethod='Cash',
            TotalAmount=sum(item['quantity'] * item['price'] for item in items)
        )

        for item in items:
            OrderItems.objects.create(
                OrderID=order,
                ItemID=item['item'],
                Quantity=item['quantity']
            )

        return order


class RegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly.")
        return old_password



class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['ItemName', 'ItemPrice', 'ItemImage']