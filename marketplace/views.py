from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import prefetch_related_objects

from marketplace.context_processors import get_cart_counter, get_cart_amounts
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor, OpeningHour


# Create your views here.


class MarketPlaceView(View):
    def get(self, request):
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        vendor_count = len(vendors)
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
        }
        return render(request, 'marketplace/vendors-list.html', context)


class VendorDetailView(View):

    def get(self, request, vendor_slug):

        vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        categories = Category.objects.filter(vendor=vendor).prefetch_related('fooditems')
        opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
        # check current day opening hour
        today_date = date.today()
        today = today_date.isoweekday()
        current_opening_hour = OpeningHour.objects.filter(vendor=vendor, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        is_open = None
        for i in current_opening_hour:
            start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
            end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
            if current_time > start and current_time < end:
                is_open = True
                break
            else:
                is_open = False
        if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user)
        else:
            cart_item = None

        context = {
            'vendor': vendor,
            'categories': categories,
            'cart_item': cart_item,
            'opening_hours': opening_hours,
            'current_opening_hour': current_opening_hour,
            'is_open': is_open,
        }
        return render(request, 'marketplace/vendor-detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.headers.get('x-request-with') == 'XMLHttpRequest':
        if request.is_ajax():
            try:
                fooditems = FoodItem.objects.get(id=food_id)
                # check if the user already added food to the card
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditems)
                    # increase cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status': "success", 'message': "increase cart quantity", "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditems, quantity=1)
                    return JsonResponse({'status': "success", 'message': "added food to the cart", "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': "failed", 'message': "this food is not available"})
        else:
            return JsonResponse({'status': "failed", 'message': "invalid request"})
    else:
        return JsonResponse({'status': "login_required", 'message': "You are not logged in"})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.headers.get('x-request-with') == 'XMLHttpRequest':
        if request.is_ajax():
            try:
                fooditems = FoodItem.objects.get(id=food_id)
                # check if the user already added food to the card
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditems)
                    # decrease cart quantity
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status': 'success', 'message': 'increase cart quantity',
                                         "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'you dont have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'this food is not available'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'You are not logged in'})


class CartView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user).order_by('created')
        context = {'cart_items': cart_items}
        return render(request, 'marketplace/cart.html', context)



def delete_from_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'item deleted', "cart_counter": get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except :
                return JsonResponse({'status': 'Failed', 'message': 'cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'invalid request'})









