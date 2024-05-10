from django.shortcuts import redirect,render
from django.http import HttpRequest, HttpResponse
from django.views import View

from vendor.models import Vendor


class Home(View):

    def get(self, request):
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        print(vendors)
        context = {
            'vendors': vendors
        }
        return render(request, "home.html", context)