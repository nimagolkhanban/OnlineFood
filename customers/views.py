from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from orders.models import Order, OrderedFood


# Create your views here.

class CustomerProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'

    def get(self, request):
        user_form = UserInfoForm(instance=request.user)
        current_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(instance=current_profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'current_profile': current_profile,
        }
        return render(request, 'customers/customer_profile.html', context)

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        current_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=current_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer-profile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            return redirect('customer-profile')

class MyOrdersView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        context = {
            'orders': orders,
        }
        return render(request, 'customers/my_orders.html', context)


class OrderDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request, order_number):
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_food = OrderedFood.objects.filter(order=order)
            subtotal = 0
            for food in ordered_food:
                subtotal += (food.price * food.quantity)
            tax = subtotal * 0.1
            grand_total = subtotal + tax
            context = {
                'order': order,
                'ordered_food': ordered_food,
                'subtotal': subtotal,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'customers/order_detail.html', context)




