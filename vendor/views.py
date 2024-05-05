from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


class RestaurantProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    profile_form = UserProfileForm
    vendor_form = VendorForm

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        # tip : instance part will complete the existing data that user fill in registration form
        profile_form = self.profile_form(instance=profile)
        vendor_form = self.vendor_form(instance=vendor)
        zone = UserProfile.objects.filter()
        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
            'current_profile': profile,
            'current_vendor': vendor,
        }
        return render(request, "vendor/vendor_profile.html", context)

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        profile_form = self.profile_form(request.POST, request.FILES, instance=profile)
        vendor_form = self.vendor_form(request.POST, request.FILES, instance=vendor)
        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
            'current_profile': profile,
            'current_vendor': vendor,

        }

        zone = request.POST.get('zone')
        profile.zone = zone
        profile.save()

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Your profile has been updated')

            return redirect("restaurant_profile")
        else:
            messages.error(request, "there is something wrong in your information")

            return render(request, "vendor/vendor_profile.html", context)


class MenuBuilderView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request):
        vendor = get_vendor(request)
        categories = Category.objects.filter(vendor=vendor)
        context = {
            'categories': categories,
        }
        return render(request, 'vendor/restaurant-menu-builder.html', context)


class FoodItemsByCategoryView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'login'
    def get(self, request, pk=None):
        vendor = get_vendor(request)
        category = get_object_or_404(Category, pk=pk)
        food_items = FoodItem.objects.filter(vendor=vendor, category=category)
        context = {
            "fooditems": food_items,
            'category': category,
        }
        return render(request, 'vendor/food_iteme_category.html', context)

















