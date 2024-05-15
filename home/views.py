from django.shortcuts import render, redirect
from django.views import View

from accounts.models import UserProfile
from home.forms import SearchForm
from vendor.models import Vendor


class Home(View):

    def get(self, request):
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        form = SearchForm()
        print(vendors)
        context = {
            'vendors': vendors,
            'search_form': form,
        }
        return render(request, "home.html", context)
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            form_restaurant_name = form.cleaned_data['restaurant_name']
            if form_restaurant_name:
                vendor = Vendor.objects.get(is_approved=True, vendor_name=form_restaurant_name)
                return redirect("vendor-detail", vendor.vendor_slug)
            else:
                return redirect("home")
        return redirect("home")



