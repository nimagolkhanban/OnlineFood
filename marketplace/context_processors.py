from decimal import Decimal, ROUND_HALF_UP

from .models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return {'cart_count': cart_count}


from decimal import Decimal, ROUND_HALF_UP


# تابع برای رند کردن Decimal با دو رقم اعشار


def get_cart_amounts(request):
    subtotal = Decimal('0.0')
    grand_total = Decimal('0.0')
    tax_rate = Decimal('0.10')
    tax = 0

    def round_decimal(value):
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditems = FoodItem.objects.get(pk=item.fooditem.pk)
            subtotal += fooditems.price * Decimal(str(item.quantity))
        tax = subtotal * tax_rate
        grand_total = subtotal + tax

        tax = round_decimal(tax)
        grand_total = round_decimal(grand_total)
        return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)

