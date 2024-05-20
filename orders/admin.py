from django.contrib import admin
from .models import Order, AccountBalance, OrderedFood
# Register your models here.

admin.site.register(Order)
admin.site.register(AccountBalance)
admin.site.register(OrderedFood)
