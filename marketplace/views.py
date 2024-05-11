from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import prefetch_related_objects

from marketplace.context_processors import get_cart_counter
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor


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
        if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user)
        else:
            cart_item = None

        context = {
            'vendor': vendor,
            'categories': categories,
            'cart_item': cart_item
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
                    return JsonResponse({'status': "success", 'message': "increase cart quantity", "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditems, quantity=1)
                    return JsonResponse({'status': "success", 'message': "added food to the cart", "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity})
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
                                         "cart_counter": get_cart_counter(request), 'qty': check_cart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'you dont have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'this food is not available'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'You are not logged in'})













