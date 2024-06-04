from django.contrib import admin
from .models import Items, OrderItems, Orders, Table2, Table1

admin.site.register(Items)
admin.site.register(OrderItems)
admin.site.register(Orders)
admin.site.register(Table1)
admin.site.register(Table2)