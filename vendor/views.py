from django.shortcuts import render, get_object_or_404
from django.views import View

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from vendor.forms import VendorForm
from vendor.models import Vendor


class RestaurantProfileView(View):
    profile_form = UserProfileForm
    vendor_form = VendorForm

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        vendor = get_object_or_404(Vendor, user=request.user)
        # tip : instance part will complete the existing data that user fill in registration form
        profile_form = self.profile_form(instance=profile)
        vendor_form = self.vendor_form(instance=vendor)

        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
            'current_profile': profile,
            'current_vendor': vendor,

        }
        return render(request, "vendor/vendor_profile.html",context)
