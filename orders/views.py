from django.shortcuts import render
from django.views import View


class PlaceOrderView(View):
    def get(self, request):
        return render(request, 'orders/place_orders.html')