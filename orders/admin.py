from django.contrib import admin
from .models import Order, AccountBalance, OrderedFood
# Register your models here.


class OrderedFoodAdmin(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'user', 'fooditem', 'quantity', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'name', 'phone', 'email', 'total', 'status', 'order_place_to', 'is_ordered')
    inlines = [OrderedFoodAdmin]


admin.site.register(Order, OrderAdmin)
admin.site.register(AccountBalance)
admin.site.register(OrderedFood)

