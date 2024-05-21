from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import prefetch_related_objects
from unicodedata import decimal

from accounts.models import UserProfile
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from marketplace.models import Cart
from menu.models import Category, FoodItem
from orders.forms import OrderForm
from orders.models import AccountBalance, OrderedFood
from vendor.models import Vendor, OpeningHour
from orders.utils import generate_order_number

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


class CheckOutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user).order_by('created')
        cart_counter = cart_items.count()
        if cart_counter == 0:
            return redirect('marketplace')
        user_profile = UserProfile.objects.get(user=request.user)
        default_value = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone_number,
            'email': request.user.email,
            'address': user_profile.address,
            'country': user_profile.country,
            'city': user_profile.city,
            'state': user_profile.state,
            'pincode': user_profile.pincode,
        }
        # tip: th bellow code is for making the form prepopulated data from db
        # we don't use instance because data is not in the one model actually initial is for adding some static default
        form = OrderForm(initial=default_value)
        context = {
            'form': form,
            'cart_items': cart_items,
            'cart_count': cart_counter,
        }
        return render(request, 'marketplace/checkout.html', context)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user).order_by('created')
        cart_counter = cart_items.count()
        form = OrderForm(request.POST)
        order_tax = get_cart_amounts(request)['tax']
        order_grand_total_price = get_cart_amounts(request)['grand_total']

        # tip: add the vendors in the order m2m relationship
        vendors_id = []
        for item in cart_items:
            if item.fooditem.vendor.id not in vendors_id:
                vendors_id.append(item.fooditem.vendor.id)

        account_balance = AccountBalance.objects.get(user=request.user)
        if account_balance.amount >= order_grand_total_price:
            account_balance.amount = account_balance.amount - float(order_grand_total_price)
            account_balance.save()
            print("done")



        if form.is_valid():
            my_order = form.save(commit=False)
            my_order.user = request.user
            my_order.tax = order_tax
            my_order.total = order_grand_total_price
            my_order.status = 'Completed'
            my_order.is_ordered = True
            my_order.save()
            # tip: we should use * and add to add the data in the m2m model, and we should do this after save because
            # order should have id to
            my_order.vendors.add(*vendors_id)
            my_order.order_number = generate_order_number(my_order.pk)
            my_order.save()
            food_in_cart = Cart.objects.filter(user=request.user)
            for food in food_in_cart:
                order_food = OrderedFood()
                order_food.order = my_order
                order_food.user = request.user
                order_food.fooditem = food.fooditem
                order_food.quantity = food.quantity
                order_food.price = food.fooditem.price
                order_food.amount = food.fooditem.price * food.quantity
                order_food.save()
                food.delete()

            return redirect('order-complete', order_number=my_order.order_number)
        else:
            context = {
                'form': form,
                'cart_items': cart_items,
                'cart_count': cart_counter,
            }
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, 'marketplace/checkout.html', context)













