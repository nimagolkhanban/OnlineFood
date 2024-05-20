from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from orders.models import Order, OrderedFood


class OrderComplete(View):
    def get(self, request, order_number):
        try:
            order_number = order_number
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_food = OrderedFood.objects.filter(order=order)
            subtotal = 0
            for food in ordered_food:
                subtotal += (food.price * food.quantity)
            tax = subtotal * 0.1
            grand_total = subtotal + tax
        except:
            messages.error(request, 'there is something wrong with your order')
            return redirect('checkout')

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'orders/order_complete.html', context)